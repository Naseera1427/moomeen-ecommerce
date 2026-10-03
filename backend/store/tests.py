from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product, Cart, CartItem


class AdminAuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Admin / staff user
        self.admin = User.objects.create_user(
            username="testadmin",
            password="Admin@Secure123",
            is_staff=True,
            is_superuser=True,
        )
        # Regular customer (no admin rights)
        self.customer = User.objects.create_user(
            username="testcustomer",
            password="Customer@123",
            is_staff=False,
            is_superuser=False,
        )

    def test_admin_login_page_is_accessible(self):
        """The dedicated admin login page must be publicly accessible."""
        response = self.client.get(reverse("admin_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_login.html")

    def test_admin_login_wrong_password_rejected(self):
        """Wrong password must not grant access and must stay on login page."""
        response = self.client.post(reverse("admin_login"), {
            "username": "testadmin",
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_login.html")
        # Must NOT be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_non_staff_account_blocked_on_admin_login(self):
        """A customer account must not be able to reach the admin dashboard via admin-login."""
        response = self.client.post(reverse("admin_login"), {
            "username": "testcustomer",
            "password": "Customer@123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_login.html")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_admin_login_success_redirects_to_dashboard(self):
        """Valid admin credentials must log in and redirect to the admin dashboard."""
        response = self.client.post(reverse("admin_login"), {
            "username": "testadmin",
            "password": "Admin@Secure123",
        }, follow=True)
        self.assertRedirects(response, reverse("admin_dashboard"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_staff)

    def test_admin_dashboard_blocked_for_unauthenticated(self):
        """Unauthenticated requests to admin URLs must redirect to admin login."""
        response = self.client.get(reverse("admin_dashboard"))
        self.assertRedirects(
            response,
            "/admin-login/?next=/admin-dashboard/",
            fetch_redirect_response=False,
        )

    def test_admin_dashboard_blocked_for_customer(self):
        """Regular customers must be blocked from admin pages and redirected to home."""
        self.client.login(username="testcustomer", password="Customer@123")
        response = self.client.get(reverse("admin_dashboard"), follow=True)
        # Should end up at home, not dashboard
        self.assertRedirects(response, reverse("home"))

    def test_admin_logout_redirects_to_admin_login(self):
        """Admin logout must end session and redirect to the admin login page."""
        self.client.login(username="testadmin", password="Admin@Secure123")
        response = self.client.post(reverse("admin_logout"), follow=True)
        self.assertRedirects(response, reverse("admin_login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_setup_admin_command_creates_staff_user(self):
        """setup_admin management command must create a staff/superuser account."""
        from django.core.management import call_command
        call_command(
            "setup_admin",
            username="newadmin",
            email="admin@moomeen.com",
            password="NewAdmin@456",
        )
        user = User.objects.get(username="newadmin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("NewAdmin@456"))


class BuyNowAndLoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.category = Category.objects.create(
            name="Health Care",
            slug="health-care"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Nellika Lehiyam",
            slug="nellika-lehiyam",
            description="Natural remedy",
            mrp=500.00,
            selling_price=450.00,
            stock=10,
            is_active=True
        )

    def test_buy_now_unauthenticated_redirects_to_login(self):
        """Unauthenticated user clicking Buy Now must redirect to Login page, not Home page."""
        response = self.client.get(reverse("buy_now", args=[self.product.id]))
        expected_redirect = f"/login/?next=/buy-now/{self.product.id}/"
        self.assertRedirects(response, expected_redirect)

    def test_login_page_invalid_credentials(self):
        """Invalid login must keep user on Login page with form errors and visible Login button."""
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertContains(response, "LOGIN")
        self.assertContains(response, "Please enter a correct username and password")

    def test_complete_buy_now_and_login_flow(self):
        """
        Unauthenticated Buy Now -> Login -> Redirect to Checkout flow.
        1. Unauthenticated user attempts Buy Now -> redirected to Login.
        2. User enters valid credentials -> logged in and redirected to buy-now endpoint.
        3. buy-now endpoint adds product to cart and redirects to Checkout page.
        """
        # Step 1: Unauthenticated request to buy_now
        buy_now_url = reverse("buy_now", args=[self.product.id])
        response1 = self.client.get(buy_now_url)
        login_url_with_next = f"/login/?next={buy_now_url}"
        self.assertRedirects(response1, login_url_with_next)

        # Step 2: Login with valid credentials and follow redirects (login -> buy_now -> checkout)
        response2 = self.client.post(login_url_with_next, {
            "username": "testuser",
            "password": "testpassword123"
        }, follow=True)
        self.assertRedirects(response2, reverse("checkout"))
        
        # Verify item is in cart
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        cart_item = cart.items.first()
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_authenticated_buy_now_redirects_directly_to_checkout(self):
        """Authenticated user clicking Buy Now goes straight to Checkout."""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(reverse("buy_now", args=[self.product.id]), {"quantity": "2"})
        self.assertRedirects(response, reverse("checkout"))
        
        cart = Cart.objects.get(user=self.user)
        cart_item = cart.items.get(product=self.product)
        self.assertEqual(cart_item.quantity, 2)
