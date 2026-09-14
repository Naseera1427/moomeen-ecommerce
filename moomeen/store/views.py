from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .forms import CheckoutAddressForm, UserLoginForm, RegisterForm

from .models import (
    Product,
    Category,
    Review,
    Address,
    Cart,
    CartItem,
    Order,
    OrderItem,
    WishlistItem,
)
def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if not request.user.is_staff:
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper

# =========================================================
# USER REGISTRATION
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "auth/register.html",
        {
            "form": form,
        }
    )


# =========================================================
# USER LOGIN
# =========================================================

def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = UserLoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

    else:

        form = UserLoginForm()

    return render(
        request,
        "auth/login.html",
        {
            "form": form,
        }
    )


# =========================================================
# USER LOGOUT
# =========================================================

@login_required
def user_logout(request):

    logout(request)

    return redirect("home")


# =========================================================
# HOME PAGE
# =========================================================

def home(request):

    categories = Category.objects.filter(
        is_active=True
    )

    featured_products = Product.objects.filter(
        is_active=True
    ).select_related(
        "category"
    ).order_by(
        "-created_at"
    )[:8]

    approved_reviews = Review.objects.filter(
        is_approved=True
    ).select_related(
        "user",
        "product"
    ).order_by(
        "-created_at"
    )[:6]

    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "featured_products": featured_products,
            "approved_reviews": approved_reviews,
        }
    )


# =========================================================
# PRODUCTS PAGE
# =========================================================

def products(request):

    product_list = Product.objects.filter(
        is_active=True
    ).select_related(
        "category"
    )

    category_slug = request.GET.get("category")
    search = request.GET.get("search")

    # Filter by category
    if category_slug:

        product_list = product_list.filter(
            category__slug=category_slug
        )

    # Search products
    if search:

        product_list = product_list.filter(
            name__icontains=search
        )

    categories = Category.objects.filter(
        is_active=True
    )

    return render(
        request,
        "products.html",
        {
            "products": product_list,
            "categories": categories,
            "search": search or "",
        }
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================

def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True
    )

    reviews = product.reviews.filter(
        is_approved=True
    ).select_related(
        "user"
    )

    # -----------------------------------------------------
    # WISHLIST CHECK
    # -----------------------------------------------------

    is_wishlisted = False

    if request.user.is_authenticated:

        is_wishlisted = WishlistItem.objects.filter(
            user=request.user,
            product=product
        ).exists()

    # -----------------------------------------------------
    # REVIEW PERMISSION
    # -----------------------------------------------------

    can_review = False
    already_reviewed = False

    if request.user.is_authenticated:

        # User must have a delivered order containing
        # this product
        can_review = OrderItem.objects.filter(
            order__user=request.user,
            order__status="DELIVERED",
            product=product
        ).exists()

        # Check whether user already submitted a review
        already_reviewed = Review.objects.filter(
            user=request.user,
            product=product
        ).exists()

    # -----------------------------------------------------
    # RENDER PRODUCT DETAIL
    # -----------------------------------------------------

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "is_wishlisted": is_wishlisted,
            "can_review": can_review,
            "already_reviewed": already_reviewed,
        }
    )

# =========================================================
# SUBMIT REVIEW
# =========================================================

@login_required
def submit_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    # Review submission must be POST
    if request.method != "POST":

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # -----------------------------------------------------
    # CHECK PURCHASE
    # -----------------------------------------------------

    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        order__status="DELIVERED",
        product=product
    ).exists()

    if not has_purchased:

        messages.error(
            request,
            "You can review this product only after it has been delivered."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # -----------------------------------------------------
    # PREVENT DUPLICATE REVIEW
    # -----------------------------------------------------

    already_reviewed = Review.objects.filter(
        user=request.user,
        product=product
    ).exists()

    if already_reviewed:

        messages.info(
            request,
            "You have already reviewed this product."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # -----------------------------------------------------
    # GET RATING
    # -----------------------------------------------------

    try:

        rating = int(
            request.POST.get("rating")
        )

    except (TypeError, ValueError):

        rating = 0

    # -----------------------------------------------------
    # GET COMMENT
    # -----------------------------------------------------

    comment = request.POST.get(
        "comment",
        ""
    ).strip()

    # -----------------------------------------------------
    # VALIDATE RATING
    # -----------------------------------------------------

    if rating < 1 or rating > 5:

        messages.error(
            request,
            "Please select a rating between 1 and 5."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # -----------------------------------------------------
    # VALIDATE COMMENT
    # -----------------------------------------------------

    if not comment:

        messages.error(
            request,
            "Please write your review."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # -----------------------------------------------------
    # CREATE REVIEW
    # -----------------------------------------------------

    Review.objects.create(
        product=product,
        user=request.user,
        rating=rating,
        comment=comment,
        is_approved=False
    )

    # -----------------------------------------------------
    # SUCCESS MESSAGE
    # -----------------------------------------------------

    messages.success(
        request,
        "Your review has been submitted and is waiting for approval."
    )

    return redirect(
        "product_detail",
        slug=product.slug
    )


# =========================================================
# ADD TO CART
# =========================================================

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    # Don't add products that are out of stock
    if product.stock <= 0:

        messages.error(
            request,
            "This product is currently out of stock."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # Get selected quantity
    try:

        quantity = int(
            request.POST.get(
                "quantity",
                1
            )
        )

    except (TypeError, ValueError):

        quantity = 1

    # Minimum quantity
    if quantity < 1:

        quantity = 1

    # Quantity cannot exceed stock
    if quantity > product.stock:

        messages.warning(
            request,
            f"Only {product.stock} item(s) are available."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # Get or create cart
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # Product already exists
    if not item_created:

        new_quantity = cart_item.quantity + quantity

        # Don't exceed stock
        if new_quantity > product.stock:

            messages.warning(
                request,
                f"You already have {cart_item.quantity} item(s) "
                f"in your cart. Only {product.stock} item(s) "
                f"are available in total."
            )

            return redirect(
                "product_detail",
                slug=product.slug
            )

        cart_item.quantity = new_quantity
        cart_item.save()

    # Product newly added
    else:

        cart_item.quantity = quantity
        cart_item.save()

    # Success message
    messages.success(
        request,
        f"{quantity} item(s) of {product.name} added to cart."
    )

    # Stay on product detail page
    return redirect(
        "product_detail",
        slug=product.slug
    )


# =========================================================
# BUY NOW
# =========================================================

@login_required
def buy_now(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    # Don't continue if out of stock
    if product.stock <= 0:

        messages.error(
            request,
            "This product is currently out of stock."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # Get selected quantity
    try:

        quantity = int(
            request.POST.get(
                "quantity",
                1
            )
        )

    except (TypeError, ValueError):

        quantity = 1

    # Minimum quantity
    if quantity < 1:

        quantity = 1

    # Quantity cannot exceed stock
    if quantity > product.stock:

        messages.warning(
            request,
            f"Only {product.stock} item(s) are available."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    # Get or create cart
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # BUY NOW uses selected quantity
    cart_item.quantity = quantity
    cart_item.save()

    # For now BUY NOW goes to cart.
    # Later this can connect directly to checkout.
    return redirect("cart")


# =========================================================
# CART
# =========================================================

@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        "product"
    )

    # Calculate subtotal from database prices
    subtotal = sum(
        item.product.selling_price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        "cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "subtotal": subtotal,
        }
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

@login_required
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect("cart")


# =========================================================
# UPDATE CART QUANTITY
# =========================================================

@login_required
def update_cart_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":

        try:

            quantity = int(
                request.POST.get(
                    "quantity",
                    1
                )
            )

        except (TypeError, ValueError):

            return redirect("cart")

        # Remove item when quantity becomes zero
        if quantity <= 0:

            cart_item.delete()

        # Update only within available stock
        elif quantity <= cart_item.product.stock:

            cart_item.quantity = quantity
            cart_item.save()

    return redirect("cart")


# =========================================================
# WISHLIST
# =========================================================

@login_required
def wishlist(request):

    wishlist_items = WishlistItem.objects.filter(
        user=request.user
    ).select_related(
        "product",
        "product__category"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "account/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


# =========================================================
# ADD TO WISHLIST
# =========================================================

@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    wishlist_item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:

        messages.success(
            request,
            f"{product.name} added to your wishlist."
        )

    else:

        messages.info(
            request,
            f"{product.name} is already in your wishlist."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "products"
        )
    )


# =========================================================
# REMOVE FROM WISHLIST
# =========================================================

@login_required
def remove_from_wishlist(request, product_id):

    wishlist_item = WishlistItem.objects.filter(
        user=request.user,
        product_id=product_id
    ).first()

    if wishlist_item:

        product_name = wishlist_item.product.name

        wishlist_item.delete()

        messages.success(
            request,
            f"{product_name} removed from your wishlist."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "wishlist"
        )
    )


# =========================================================
# CHECKOUT
# =========================================================

@login_required
def checkout(request):

    # Get user's cart
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        "product"
    )

    # -----------------------------------------------------
    # EMPTY CART CHECK
    # -----------------------------------------------------

    if not cart_items.exists():

        messages.warning(
            request,
            "Your cart is empty. Please add a product before checkout."
        )

        return redirect("products")

    # -----------------------------------------------------
    # STOCK VALIDATION
    # -----------------------------------------------------

    for item in cart_items:

        if item.product.stock <= 0:

            messages.error(
                request,
                f"{item.product.name} is currently out of stock."
            )

            return redirect("cart")

        if item.quantity > item.product.stock:

            messages.error(
                request,
                f"Only {item.product.stock} item(s) of "
                f"{item.product.name} are available."
            )

            return redirect("cart")

    # -----------------------------------------------------
    # RECALCULATE SUBTOTAL FROM DATABASE
    # -----------------------------------------------------

    subtotal = sum(
        item.product.selling_price * item.quantity
        for item in cart_items
    )

    # -----------------------------------------------------
    # SHIPPING CHARGE
    # -----------------------------------------------------

    # Temporary checkout shipping rule.
    # We can change this later based on the company's
    # actual shipping policy.

    shipping_charge = 0

    # -----------------------------------------------------
    # FINAL TOTAL
    # -----------------------------------------------------

    total_amount = subtotal + shipping_charge

    # -----------------------------------------------------
    # GET DEFAULT ADDRESS
    # -----------------------------------------------------

    default_address = Address.objects.filter(
        user=request.user,
        is_default=True
    ).first()

    # -----------------------------------------------------
    # CHECKOUT FORM
    # -----------------------------------------------------

    if request.method == "POST":

        form = CheckoutAddressForm(
            request.POST
        )

        if form.is_valid():

            address = form.save(
                commit=False
            )

            address.user = request.user

            # New checkout address is not automatically
            # made default.
            address.is_default = False

            address.save()

            # -------------------------------------------------
            # CREATE ORDER NUMBER
            # -------------------------------------------------

            import uuid

            order_number = (
                "MP-"
                + uuid.uuid4().hex[:10].upper()
            )

            # -------------------------------------------------
            # CREATE ORDER
            # -------------------------------------------------

            order = Order.objects.create(

                user=request.user,

                order_number=order_number,

                full_name=address.full_name,

                phone=address.phone,

                address=address.address_line,

                city=address.city,

                state=address.state,

                pincode=address.pincode,

                subtotal=subtotal,

                shipping_charge=shipping_charge,

                total_amount=total_amount,

                status="PLACED",

                # CURRENTLY COD ONLY
                payment_method="COD",

                payment_status="Pending",
            )

            # -------------------------------------------------
            # CREATE ORDER ITEMS
            # -------------------------------------------------

            for item in cart_items:

                OrderItem.objects.create(

                    order=order,

                    product=item.product,

                    product_name=item.product.name,

                    quantity=item.quantity,

                    price=item.product.selling_price,
                )

            # -------------------------------------------------
            # REDUCE STOCK
            # -------------------------------------------------

            for item in cart_items:

                item.product.stock -= item.quantity

                item.product.save(
                    update_fields=["stock"]
                )

            # -------------------------------------------------
            # CLEAR CART
            # -------------------------------------------------

            cart.items.all().delete()

            # -------------------------------------------------
            # GO TO ORDER CONFIRMATION
            # -------------------------------------------------

            return redirect(
                "order_confirmation",
                order_number=order.order_number
            )

    else:

        # Pre-fill checkout form with default address
        if default_address:

            form = CheckoutAddressForm(
                instance=default_address
            )

        else:

            form = CheckoutAddressForm(
                initial={
                    "full_name": request.user.get_full_name(),
                    "phone": "",
                }
            )

    # -----------------------------------------------------
    # RENDER CHECKOUT
    # -----------------------------------------------------

    return render(
        request,
        "checkout.html",
        {
            "form": form,
            "cart": cart,
            "cart_items": cart_items,
            "subtotal": subtotal,
            "shipping_charge": shipping_charge,
            "total_amount": total_amount,
            "default_address": default_address,
        }
    )


# =========================================================
# ORDER CONFIRMATION
# =========================================================

@login_required
def order_confirmation(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    return render(
        request,
        "order_confirmation.html",
        {
            "order": order,
        }
    )


# =========================================================
# MY ORDERS
# =========================================================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders,
        }
    )


# =========================================================
# ABOUT PAGE
# =========================================================

def about(request):

    return render(
        request,
        "about.html"
    )


# =========================================================
# CONTACT PAGE
# =========================================================

def contact(request):

    return render(
        request,
        "contact.html"
    )

# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
def admin_dashboard(request):

    # Only staff/admin users can access
    if not request.user.is_staff:
        return redirect("home")

    # -----------------------------------------------------
    # BASIC STATISTICS
    # -----------------------------------------------------

    total_orders = Order.objects.count()

    total_products = Product.objects.filter(
        is_active=True
    ).count()

    total_customers = User.objects.filter(
        is_staff=False
    ).count()

    # -----------------------------------------------------
    # PENDING ORDERS
    # -----------------------------------------------------

    pending_orders = Order.objects.filter(
        status__in=[
            "PLACED",
            "CONFIRMED",
            "PACKED",
            "SHIPPED",
            "OUT_FOR_DELIVERY",
        ]
    ).count()

    # -----------------------------------------------------
    # LOW STOCK PRODUCTS
    # -----------------------------------------------------

    low_stock_products = Product.objects.filter(
        is_active=True,
        stock__gt=0,
        stock__lte=5
    ).count()

    # -----------------------------------------------------
    # TOTAL SALES
    # -----------------------------------------------------

    total_sales = Order.objects.filter(
        status="DELIVERED"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    # -----------------------------------------------------
    # RECENT ORDERS
    # -----------------------------------------------------

    recent_orders = Order.objects.select_related(
        "user"
    ).order_by(
        "-created_at"
    )[:10]

    # -----------------------------------------------------
    # RENDER DASHBOARD
    # -----------------------------------------------------

    return render(
        request,
        "admin/dashboard.html",
        {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "total_products": total_products,
            "total_customers": total_customers,
            "low_stock_products": low_stock_products,
            "total_sales": total_sales,
            "recent_orders": recent_orders,
        }
    )
# =====================================================
# ADMIN PRODUCT MANAGEMENT
# =====================================================

@login_required
def admin_products(request):
    if not request.user.is_staff:
        return redirect("home")

    product_list = Product.objects.select_related(
        "category"
    ).order_by("-created_at")

    search = request.GET.get("search", "").strip()
    selected_category = request.GET.get("category", "")
    selected_status = request.GET.get("status", "")

    if search:
        product_list = product_list.filter(
            name__icontains=search
        )

    if selected_category:
        product_list = product_list.filter(
            category_id=selected_category
        )

    if selected_status == "active":
        product_list = product_list.filter(
            is_active=True
        )

    elif selected_status == "inactive":
        product_list = product_list.filter(
            is_active=False
        )

    categories = Category.objects.filter(
        is_active=True
    ).order_by("name")

    return render(
        request,
        "admin/products.html",
        {
            "products": product_list,
            "categories": categories,
            "search": search,
            "selected_category": selected_category,
            "selected_status": selected_status,
        }
    )


@login_required
def admin_product_add(request):
    if not request.user.is_staff:
        return redirect("home")

    categories = Category.objects.filter(
        is_active=True
    ).order_by("name")

    if request.method == "POST":

        category_id = request.POST.get("category")
        name = request.POST.get("name", "").strip()
        slug = request.POST.get("slug", "").strip()
        short_description = request.POST.get(
            "short_description", ""
        ).strip()
        description = request.POST.get(
            "description", ""
        ).strip()
        ingredients = request.POST.get(
            "ingredients", ""
        ).strip()
        directions = request.POST.get(
            "directions", ""
        ).strip()
        precautions = request.POST.get(
            "precautions", ""
        ).strip()
        storage = request.POST.get(
            "storage", ""
        ).strip()
        net_quantity = request.POST.get(
            "net_quantity", ""
        ).strip()

        mrp = request.POST.get("mrp", "").strip()
        selling_price = request.POST.get(
            "selling_price", ""
        ).strip()
        stock = request.POST.get("stock", "").strip()

        image = request.FILES.get("image")

        is_active = request.POST.get("is_active") == "on"

        if not category_id or not name or not slug or not description:
            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "admin/product_form.html",
                {
                    "categories": categories,
                    "form_type": "add",
                }
            )

        if Product.objects.filter(slug=slug).exists():
            messages.error(
                request,
                "A product with this slug already exists."
            )

            return render(
                request,
                "admin/product_form.html",
                {
                    "categories": categories,
                    "form_type": "add",
                }
            )

        product = Product.objects.create(
            category_id=category_id,
            name=name,
            slug=slug,
            short_description=short_description,
            description=description,
            ingredients=ingredients,
            directions=directions,
            precautions=precautions,
            storage=storage,
            net_quantity=net_quantity,
            mrp=mrp,
            selling_price=selling_price,
            stock=stock,
            image=image,
            is_active=is_active,
        )

        messages.success(
            request,
            f"{product.name} added successfully."
        )

        return redirect("admin_products")

    return render(
        request,
        "admin/product_form.html",
        {
            "categories": categories,
            "form_type": "add",
        }
    )


@login_required
def admin_product_edit(request, product_id):
    if not request.user.is_staff:
        return redirect("home")

    product = get_object_or_404(
        Product,
        id=product_id
    )

    categories = Category.objects.filter(
        is_active=True
    ).order_by("name")

    if request.method == "POST":

        category_id = request.POST.get("category")
        name = request.POST.get("name", "").strip()
        slug = request.POST.get("slug", "").strip()
        short_description = request.POST.get(
            "short_description", ""
        ).strip()
        description = request.POST.get(
            "description", ""
        ).strip()
        ingredients = request.POST.get(
            "ingredients", ""
        ).strip()
        directions = request.POST.get(
            "directions", ""
        ).strip()
        precautions = request.POST.get(
            "precautions", ""
        ).strip()
        storage = request.POST.get(
            "storage", ""
        ).strip()
        net_quantity = request.POST.get(
            "net_quantity", ""
        ).strip()

        mrp = request.POST.get("mrp", "").strip()
        selling_price = request.POST.get(
            "selling_price", ""
        ).strip()
        stock = request.POST.get("stock", "").strip()

        image = request.FILES.get("image")

        is_active = request.POST.get("is_active") == "on"

        if not category_id or not name or not slug or not description:
            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "admin/product_form.html",
                {
                    "product": product,
                    "categories": categories,
                    "form_type": "edit",
                }
            )

        if Product.objects.filter(
            slug=slug
        ).exclude(
            id=product.id
        ).exists():

            messages.error(
                request,
                "Another product is already using this slug."
            )

            return render(
                request,
                "admin/product_form.html",
                {
                    "product": product,
                    "categories": categories,
                    "form_type": "edit",
                }
            )

        product.category_id = category_id
        product.name = name
        product.slug = slug
        product.short_description = short_description
        product.description = description
        product.ingredients = ingredients
        product.directions = directions
        product.precautions = precautions
        product.storage = storage
        product.net_quantity = net_quantity
        product.mrp = mrp
        product.selling_price = selling_price
        product.stock = stock
        product.is_active = is_active

        if image:
            product.image = image

        product.save()

        messages.success(
            request,
            f"{product.name} updated successfully."
        )

        return redirect("admin_products")

    return render(
        request,
        "admin/product_form.html",
        {
            "product": product,
            "categories": categories,
            "form_type": "edit",
        }
    )
# =====================================================
# ADMIN ORDER MANAGEMENT
# =====================================================

@login_required
def admin_orders(request):
    if not request.user.is_staff:
        return redirect("home")

    orders = Order.objects.select_related(
        "user"
    ).order_by("-created_at")

    search = request.GET.get("search", "").strip()
    selected_status = request.GET.get("status", "").strip()

    if search:
        orders = orders.filter(
            order_number__icontains=search
        ) | orders.filter(
            full_name__icontains=search
        ) | orders.filter(
            phone__icontains=search
        )

    if selected_status:
        orders = orders.filter(
            status=selected_status
        )

    return render(
        request,
        "admin/orders.html",
        {
            "orders": orders,
            "search": search,
            "selected_status": selected_status,
            "status_choices": Order.STATUS_CHOICES,
        }
    )


@login_required
def admin_order_detail(request, order_id):
    if not request.user.is_staff:
        return redirect("home")
    order = get_object_or_404(
    Order.objects.select_related(
        "user"
    ),
    id=order_id
   )

    if request.method == "POST":

        new_status = request.POST.get("status", "").strip()

        valid_statuses = [
            choice[0]
            for choice in Order.STATUS_CHOICES
        ]

        if new_status not in valid_statuses:
            messages.error(
                request,
                "Invalid order status."
            )

            return redirect(
                "admin_order_detail",
                order_id=order.id
            )

        order.status = new_status

        # Payment status update
        if new_status == "DELIVERED":
            order.payment_status = "Paid"

        elif new_status == "CANCELLED":
            order.payment_status = "Cancelled"

        order.save()

        messages.success(
            request,
            f"Order {order.order_number} updated successfully."
        )

        return redirect(
            "admin_order_detail",
            order_id=order.id
        )

    return render(
        request,
        "admin/order_detail.html",
        {
            "order": order,
        }
    )
# =========================================================
# ADMIN CUSTOMER MANAGEMENT
# =========================================================

@login_required
def admin_customers(request):
    if not request.user.is_staff:
        return redirect("home")

    customers = User.objects.filter(
        is_staff=False
    ).order_by("-date_joined")

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = request.GET.get("search", "").strip()

    if search:
        customers = customers.filter(
            first_name__icontains=search
        ) | customers.filter(
            last_name__icontains=search
        ) | customers.filter(
            username__icontains=search
        ) | customers.filter(
            email__icontains=search
        )

    # -----------------------------------------------------
    # CUSTOMER ORDER COUNT + TOTAL PURCHASE
    # -----------------------------------------------------

    customers = customers.annotate(
        order_count=Count("orders", distinct=True),
        total_purchase=Sum(
            "orders__total_amount",
            distinct=True
        )
    )

    return render(
        request,
        "admin/customers.html",
        {
            "customers": customers,
            "search": search,
        }
    )


# =========================================================
# ADMIN CUSTOMER DETAIL
# =========================================================

@login_required
def admin_customer_detail(request, customer_id):
    if not request.user.is_staff:
        return redirect("home")

    customer = get_object_or_404(
        User,
        id=customer_id,
        is_staff=False
    )

    # -----------------------------------------------------
    # CUSTOMER ORDERS
    # -----------------------------------------------------

    orders = Order.objects.filter(
        user=customer
    ).order_by(
        "-created_at"
    )

    # -----------------------------------------------------
    # CUSTOMER ADDRESSES
    # -----------------------------------------------------

    addresses = Address.objects.filter(
        user=customer
    ).order_by(
        "-is_default",
        "-id"
    )

    # -----------------------------------------------------
    # CUSTOMER TOTALS
    # -----------------------------------------------------

    order_count = orders.count()

    total_purchase = orders.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    # -----------------------------------------------------
    # CUSTOMER REVIEWS
    # -----------------------------------------------------

    reviews = Review.objects.filter(
        user=customer
    ).select_related(
        "product"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "admin/customer_detail.html",
        {
            "customer": customer,
            "orders": orders,
            "addresses": addresses,
            "order_count": order_count,
            "total_purchase": total_purchase,
            "reviews": reviews,
        }
    )


# =========================================================
# ACTIVATE / DEACTIVATE CUSTOMER
# =========================================================

@login_required
def admin_toggle_customer(request, customer_id):
    if not request.user.is_staff:
        return redirect("home")

    customer = get_object_or_404(
        User,
        id=customer_id,
        is_staff=False
    )

    if request.method == "POST":

        customer.is_active = not customer.is_active

        customer.save(
            update_fields=["is_active"]
        )

        if customer.is_active:
            messages.success(
                request,
                f"{customer.username} account activated successfully."
            )
        else:
            messages.success(
                request,
                f"{customer.username} account deactivated successfully."
            )

    return redirect(
        "admin_customer_detail",
        customer_id=customer.id
    )
# =========================================================
# ADMIN REVIEW MANAGEMENT
# =========================================================

@admin_required
def admin_reviews(request):

    reviews = Review.objects.select_related(
        "user",
        "product"
    ).order_by(
        "-created_at"
    )

    search = request.GET.get("search", "").strip()
    selected_status = request.GET.get("status", "").strip()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search:
        reviews = reviews.filter(
            Q(product__name__icontains=search)
            | Q(user__username__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(comment__icontains=search)
        )

    # -----------------------------------------------------
    # STATUS FILTER
    # -----------------------------------------------------

    if selected_status == "approved":

        reviews = reviews.filter(
            is_approved=True
        )

    elif selected_status == "pending":

        reviews = reviews.filter(
            is_approved=False
        )

    return render(
        request,
        "admin/reviews.html",
        {
            "reviews": reviews,
            "search": search,
            "selected_status": selected_status,
        }
    )


# =========================================================
# APPROVE / HIDE REVIEW
# =========================================================

@admin_required
def admin_toggle_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id
    )

    if request.method == "POST":

        review.is_approved = not review.is_approved

        review.save(
            update_fields=["is_approved"]
        )

        if review.is_approved:

            messages.success(
                request,
                "Review approved successfully."
            )

        else:

            messages.success(
                request,
                "Review hidden successfully."
            )

    return redirect("admin_reviews")


# =========================================================
# DELETE REVIEW
# =========================================================

@admin_required
def admin_delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id
    )

    if request.method == "POST":

        review.delete()

        messages.success(
            request,
            "Review deleted successfully."
        )

    return redirect("admin_reviews")