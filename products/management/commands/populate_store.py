from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product
from decimal import Decimal
import uuid

class Command(BaseCommand):
    help = 'Populate database with fitness supplement categories and products'

    def handle(self, *args, **options):
        self.stdout.write("Creating categories...")
        self.create_categories()
        
        self.stdout.write("Creating products...")
        self.create_products()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated store!'))

    def create_categories(self):
        categories_data = [
            {
                'name': 'Protein Supplements',
                'description': 'High-quality protein powders, bars, and shakes for muscle building and recovery'
            },
            {
                'name': 'Pre-Workout',
                'description': 'Energy and focus supplements to enhance your training performance'
            },
            {
                'name': 'Creatine',
                'description': 'Strength and power enhancement supplements for explosive performance'
            },
            {
                'name': 'Vitamins & Minerals',
                'description': 'Essential nutrients, multivitamins, and mineral supplements'
            },
            {
                'name': 'Fat Burners',
                'description': 'Weight management and metabolism support supplements'
            },
            {
                'name': 'Post-Workout Recovery',
                'description': 'Recovery supplements for muscle repair and reduced soreness'
            },
            {
                'name': 'Amino Acids',
                'description': 'Essential and branched-chain amino acids for muscle support'
            },
            {
                'name': 'Health & Wellness',
                'description': 'General health supplements for overall wellness and vitality'
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slugify(cat_data['name']),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")

    def create_products(self):
        products_data = [
            # Protein Supplements
            {
                'name': 'Gold Standard 100% Whey Protein',
                'category': 'Protein Supplements',
                'description': 'The world\'s best-selling whey protein powder. 24g of protein per serving with 5.5g of naturally occurring BCAAs and 4g of naturally occurring glutamine.',
                'short_description': 'Premium whey protein with 24g protein per serving',
                'price': Decimal('59.99'),
                'compare_price': Decimal('69.99'),
                'stock_quantity': 150,
            },
            {
                'name': 'Casein Protein Powder',
                'category': 'Protein Supplements',
                'description': 'Slow-digesting protein perfect for nighttime recovery. Rich, creamy texture that mixes easily and tastes great.',
                'short_description': 'Slow-release protein for overnight recovery',
                'price': Decimal('49.99'),
                'compare_price': Decimal('59.99'),
                'stock_quantity': 85,
            },
            {
                'name': 'Plant-Based Protein Blend',
                'category': 'Protein Supplements',
                'description': 'Complete vegan protein from organic pea, brown rice, and hemp. 25g protein per serving, naturally flavored and sweetened.',
                'short_description': 'Organic vegan protein blend with 25g protein',
                'price': Decimal('44.99'),
                'compare_price': Decimal('54.99'),
                'stock_quantity': 120,
            },
            
            # Pre-Workout
            {
                'name': 'C4 Original Pre-Workout',
                'category': 'Pre-Workout',
                'description': 'Explosive energy, heightened focus, and an overwhelming urge to tackle any challenge. Contains CarnoSyn Beta-Alanine, Creatine Nitrate, and Caffeine.',
                'short_description': 'Explosive pre-workout with beta-alanine and caffeine',
                'price': Decimal('34.99'),
                'compare_price': Decimal('39.99'),
                'stock_quantity': 200,
            },
            {
                'name': 'Nitric Oxide Booster',
                'category': 'Pre-Workout',
                'description': 'Enhance blood flow and muscle pumps with L-Arginine, Citrulline Malate, and Beetroot Extract. Stimulant-free formula.',
                'short_description': 'Stimulant-free pump enhancement formula',
                'price': Decimal('39.99'),
                'compare_price': Decimal('44.99'),
                'stock_quantity': 75,
            },
            
            # Creatine
            {
                'name': 'Creatine Monohydrate Powder',
                'category': 'Creatine',
                'description': 'Pure, micronized creatine monohydrate for increased strength, power, and lean muscle mass. Unflavored and easily mixable.',
                'short_description': 'Pure micronized creatine monohydrate',
                'price': Decimal('24.99'),
                'compare_price': Decimal('29.99'),
                'stock_quantity': 300,
            },
            {
                'name': 'Creatine HCL Capsules',
                'category': 'Creatine',
                'description': 'Highly concentrated creatine hydrochloride in convenient capsule form. No loading phase required, better absorption.',
                'short_description': 'Fast-absorbing creatine HCL capsules',
                'price': Decimal('29.99'),
                'compare_price': Decimal('34.99'),
                'stock_quantity': 180,
            },
            
            # Vitamins & Minerals
            {
                'name': 'Men\'s Daily Multivitamin',
                'category': 'Vitamins & Minerals',
                'description': 'Complete daily vitamin and mineral support formulated specifically for active men. Includes antioxidants and energy support.',
                'short_description': 'Complete daily nutrition for active men',
                'price': Decimal('19.99'),
                'compare_price': Decimal('24.99'),
                'stock_quantity': 250,
            },
            {
                'name': 'Vitamin D3 + K2',
                'category': 'Vitamins & Minerals',
                'description': 'High-potency Vitamin D3 (5000 IU) with Vitamin K2 for bone health, immune function, and calcium absorption.',
                'short_description': 'High-potency D3 + K2 for bone health',
                'price': Decimal('16.99'),
                'compare_price': Decimal('21.99'),
                'stock_quantity': 400,
            },
            
            # Fat Burners
            {
                'name': 'Thermogenic Fat Burner',
                'category': 'Fat Burners',
                'description': 'Advanced thermogenic formula with green tea extract, caffeine, and L-Carnitine to support metabolism and energy.',
                'short_description': 'Advanced thermogenic metabolism support',
                'price': Decimal('42.99'),
                'compare_price': Decimal('49.99'),
                'stock_quantity': 90,
            },
            
            # Post-Workout Recovery
            {
                'name': 'BCAA Recovery Formula',
                'category': 'Post-Workout Recovery',
                'description': 'Essential amino acids in the optimal 2:1:1 ratio of leucine, isoleucine, and valine for muscle recovery and growth.',
                'short_description': '2:1:1 BCAA ratio for optimal recovery',
                'price': Decimal('32.99'),
                'compare_price': Decimal('37.99'),
                'stock_quantity': 160,
            },
            
            # Amino Acids
            {
                'name': 'L-Glutamine Powder',
                'category': 'Amino Acids',
                'description': 'Pure L-Glutamine to support muscle recovery, immune function, and gut health. Unflavored and easily mixable.',
                'short_description': 'Pure L-Glutamine for recovery and immunity',
                'price': Decimal('22.99'),
                'compare_price': Decimal('27.99'),
                'stock_quantity': 220,
            },
            
            # Health & Wellness
            {
                'name': 'Omega-3 Fish Oil',
                'category': 'Health & Wellness',
                'description': 'High-potency EPA and DHA omega-3 fatty acids for heart health, brain function, and inflammation support.',
                'short_description': 'High-potency omega-3 for heart and brain health',
                'price': Decimal('28.99'),
                'compare_price': Decimal('34.99'),
                'stock_quantity': 180,
            },
            {
                'name': 'Probiotics Complex',
                'category': 'Health & Wellness',
                'description': '50 billion CFU with 10 diverse probiotic strains for digestive health, immune support, and gut microbiome balance.',
                'short_description': '50 billion CFU probiotic complex',
                'price': Decimal('35.99'),
                'compare_price': Decimal('42.99'),
                'stock_quantity': 140,
            }
        ]
        
        for product_data in products_data:
            try:
                category = Category.objects.get(name=product_data['category'])
                
                # Generate a unique SKU
                sku = f"FS-{str(uuid.uuid4())[:8].upper()}"
                
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'category': category,
                        'slug': slugify(product_data['name']),
                        'description': product_data['description'],
                        'short_description': product_data['short_description'],
                        'price': product_data['price'],
                        'compare_price': product_data['compare_price'],
                        'stock_quantity': product_data['stock_quantity'],
                        'sku': sku,
                        'is_active': True,
                        'is_featured': False,

                    }
                )
                
                if created:
                    self.stdout.write(f"Created product: {product.name} (SKU: {sku})")
                    
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Category '{product_data['category']}' not found")
                )