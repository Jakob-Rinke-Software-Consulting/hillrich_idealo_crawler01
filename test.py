from item_filter.amazon_product import AmazonProduct
import item_filter.amazon_fba_calculator as amazon_fba_calculator
import item_filter.amazon_local_fba_calculator as amazon_local_fba_calculator


test_product = AmazonProduct("https://www.amazon.de/dp/B0BNM2DPDP", 644.99)

print("FBA Costs (old):", amazon_fba_calculator.get_shipping_fees(test_product, 400.2, 644.99))
print("FBA Costs (local):", amazon_local_fba_calculator.get_shipping_fees(test_product, 400.2, 644.99))


