"""
Seed script to populate database with test data.
Run: python -m app.seed_data
Force reseed: python -m app.seed_data --force
"""
import sys
from app.database import SessionLocal, initialize_database
from app.models import UserAccount, SweetProduct
from app.auth.password_hasher import hash_password


def clear_database(db):
    """Clear all data from database."""
    db.query(SweetProduct).delete()
    db.query(UserAccount).delete()
    db.commit()
    print("🗑️ Cleared existing data")


def seed_database(force=False):
    """Populate database with test data."""
    initialize_database()
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(SweetProduct).count() > 0:
            if force:
                clear_database(db)
            else:
                print("⚠️ Database already has data. Use --force to reseed.")
                return
        
        # Create admin user
        admin = UserAccount(
            email_address="admin@sweetshop.com",
            full_name="Shop Admin",
            hashed_password=hash_password("admin123"),
            is_administrator=True
        )
        db.add(admin)
        
        # Create regular user
        user = UserAccount(
            email_address="user@sweetshop.com",
            full_name="Regular Customer",
            hashed_password=hash_password("user1234"),
            is_administrator=False
        )
        db.add(user)
        
        # Create test sweets with INR prices
        sweets = [
            SweetProduct(
                sweet_name="Kaju Katli",
                sweet_category="Traditional",
                sweet_price=450.00,  # ₹450 per kg
                quantity_in_stock=50,
                sweet_description="Premium cashew fudge with silver foil"
            ),
            SweetProduct(
                sweet_name="Chocolate Truffle",
                sweet_category="Chocolate",
                sweet_price=299.00,  # ₹299
                quantity_in_stock=50,
                sweet_description="Rich dark chocolate truffles with creamy center"
            ),
            SweetProduct(
                sweet_name="Gulab Jamun",
                sweet_category="Traditional",
                sweet_price=180.00,  # ₹180 per kg
                quantity_in_stock=75,
                sweet_description="Soft milk dumplings in sugar syrup"
            ),
            SweetProduct(
                sweet_name="Gummy Bears",
                sweet_category="Gummy",
                sweet_price=120.00,  # ₹120
                quantity_in_stock=200,
                sweet_description="Colorful fruit-flavored gummy bears"
            ),
            SweetProduct(
                sweet_name="Rasgulla",
                sweet_category="Traditional",
                sweet_price=220.00,  # ₹220 per kg
                quantity_in_stock=100,
                sweet_description="Spongy cottage cheese balls in sugar syrup"
            ),
            SweetProduct(
                sweet_name="Strawberry Lollipop",
                sweet_category="Lollipop",
                sweet_price=20.00,  # ₹20 each
                quantity_in_stock=150,
                sweet_description="Sweet strawberry flavored lollipops"
            ),
            SweetProduct(
                sweet_name="Soan Papdi",
                sweet_category="Traditional",
                sweet_price=160.00,  # ₹160 per box
                quantity_in_stock=40,
                sweet_description="Flaky crispy sweet with cardamom"
            ),
            SweetProduct(
                sweet_name="Jalebi",
                sweet_category="Traditional",
                sweet_price=140.00,  # ₹140 per kg
                quantity_in_stock=180,
                sweet_description="Crispy spiral sweets soaked in syrup"
            ),
            SweetProduct(
                sweet_name="Dairy Milk Silk",
                sweet_category="Chocolate",
                sweet_price=85.00,  # ₹85
                quantity_in_stock=60,
                sweet_description="Smooth and creamy milk chocolate"
            ),
            SweetProduct(
                sweet_name="Cotton Candy",
                sweet_category="Candy",
                sweet_price=50.00,  # ₹50
                quantity_in_stock=0,  # Out of stock!
                sweet_description="Fluffy pink cotton candy"
            ),
            SweetProduct(
                sweet_name="Motichoor Ladoo",
                sweet_category="Traditional",
                sweet_price=280.00,  # ₹280 per kg
                quantity_in_stock=250,
                sweet_description="Fine boondi ladoos with nuts"
            ),
            SweetProduct(
                sweet_name="5 Star Chocolate",
                sweet_category="Chocolate",
                sweet_price=25.00,  # ₹25
                quantity_in_stock=120,
                sweet_description="Classic caramel filled chocolate bar"
            ),
            SweetProduct(
                sweet_name="Mysore Pak",
                sweet_category="Traditional",
                sweet_price=320.00,  # ₹320 per kg
                quantity_in_stock=90,
                sweet_description="Rich gram flour sweet with ghee"
            ),
            SweetProduct(
                sweet_name="Barfi Mix",
                sweet_category="Traditional",
                sweet_price=380.00,  # ₹380 per kg
                quantity_in_stock=45,
                sweet_description="Assorted barfi - kaju, pista, badam"
            ),
        ]
        
        for sweet in sweets:
            db.add(sweet)
        
        db.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   📧 Admin: admin@sweetshop.com / admin123")
        print(f"   📧 User: user@sweetshop.com / user1234")
        print(f"   🍬 Added {len(sweets)} sweets to inventory")
        print(f"   💰 Prices in INR (₹)")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    force = "--force" in sys.argv
    seed_database(force=force)