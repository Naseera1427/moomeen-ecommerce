from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # =====================================================
    # ADMIN PRODUCT MANAGEMENT
    # =====================================================

    path(
        "admin-products/",
        views.admin_products,
        name="admin_products"
    ),

    path(
        "admin-products/add/",
        views.admin_product_add,
        name="admin_product_add"
    ),

    path(
        "admin-products/edit/<int:product_id>/",
        views.admin_product_edit,
        name="admin_product_edit"
    ),


    # =====================================================
    # USER AUTHENTICATION
    # =====================================================

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),


    # =====================================================
    # PRODUCTS
    # =====================================================

    path(
        "products/",
        views.products,
        name="products"
    ),

    path(
        "products/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "products/<int:product_id>/review/",
        views.submit_review,
        name="submit_review"
    ),


    # =====================================================
    # CART
    # =====================================================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "cart/update/<int:item_id>/",
        views.update_cart_quantity,
        name="update_cart_quantity"
    ),


    # =====================================================
    # BUY NOW
    # =====================================================

    path(
        "buy-now/<int:product_id>/",
        views.buy_now,
        name="buy_now"
    ),


    # =====================================================
    # WISHLIST
    # =====================================================

    path(
        "wishlist/",
        views.wishlist,
        name="wishlist"
    ),

    path(
        "wishlist/add/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "wishlist/remove/<int:product_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),


    # =====================================================
    # CHECKOUT
    # =====================================================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "order-confirmation/<str:order_number>/",
        views.order_confirmation,
        name="order_confirmation"
    ),

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),


    # =====================================================
    # COMPANY
    # =====================================================

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),
    path(
    "admin-orders/",
    views.admin_orders,
    name="admin_orders"
),

path(
    "admin-orders/<int:order_id>/",
    views.admin_order_detail,
    name="admin_order_detail"
),
path(
    "admin-customers/",
    views.admin_customers,
    name="admin_customers"
),

path(
    "admin-customers/<int:customer_id>/",
    views.admin_customer_detail,
    name="admin_customer_detail"
),

path(
    "admin-customers/<int:customer_id>/toggle/",
    views.admin_toggle_customer,
    name="admin_toggle_customer"
),

path("admin-reviews/",
      views.admin_reviews,
        name="admin_reviews"
        ),
path("admin-reviews/<int:review_id>/toggle/", 
     views.admin_toggle_review,
       name="admin_toggle_review"
       ),
path("admin-reviews/<int:review_id>/delete/",
      views.admin_delete_review, 
      name="admin_delete_review"
      ),

]