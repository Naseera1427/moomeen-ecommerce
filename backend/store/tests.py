from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product, Cart, CartItem


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
