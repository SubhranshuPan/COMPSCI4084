# Each loaf - 3.49
# Discount - 0.60

# Number of loaves purchased: Given 
# To Display:
        # regular price
        # discount
        # final price
# Each amount in its own line , with appropriate label

reg_price = 3.49
discount = 0.60

num_loaves = int(input("Enter number of loaves purchased: "))
regular_price = num_loaves * reg_price
discount_price = regular_price * discount
final_price = regular_price - discount_price

print(f"Regular price: £{regular_price:.2f}")
print(f"Discount (60%): £{discount_price:.2f}")
print(f"Final Price: £{final_price:.2f}")

