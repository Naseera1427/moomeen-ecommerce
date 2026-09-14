from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# =========================
# CATEGORY
# =========================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# =========================
# PRODUCT
# =========================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True
    )

    short_description = models.TextField(
        blank=True
    )

    description = models.TextField()

    ingredients = models.TextField(
        blank=True
    )

    directions = models.TextField(
        blank=True
    )

    precautions = models.TextField(
        blank=True
    )

    storage = models.TextField(
        blank=True
    )

    net_quantity = models.CharField(
        max_length=100,
        blank=True
    )

    mrp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):

        if self.mrp > self.selling_price:

            return round(
                ((self.mrp - self.selling_price) / self.mrp) * 100
            )

        return 0


# =========================
# PRODUCT IMAGE
# =========================

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/gallery/"
    )

    is_primary = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.product.name} image"


# =========================
# REVIEW
# =========================

class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    comment = models.TextField()

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} - {self.rating}/5"


# =========================
# ADDRESS
# =========================

class Address(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    address_line = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    is_default = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.full_name} - {self.city}"


# =========================
# WISHLIST
# =========================

class WishlistItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# =========================
# ORDER
# =========================

class Order(models.Model):

    STATUS_CHOICES = [
        ("PLACED", "Placed"),
        ("CONFIRMED", "Confirmed"),
        ("PACKED", "Packed"),
        ("SHIPPED", "Shipped"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("COD", "Cash on Delivery"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_number = models.CharField(
        max_length=30,
        unique=True
    )

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    shipping_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="PLACED"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="COD"
    )

    payment_status = models.CharField(
        max_length=30,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.order_number


# =========================
# ORDER ITEM
# =========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    product_name = models.CharField(
        max_length=200
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.order.order_number} - {self.product_name}"


# =========================
# CART
# =========================

class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Cart - {self.user.username}"


# =========================
# CART ITEM
# =========================

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    @property
    def total_price(self):
        return self.product.selling_price * self.quantity

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"