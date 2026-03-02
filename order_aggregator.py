input_file = "orders.txt"
output_file = "summary_report.txt"
error_log = "error_log.txt"
agg_data = {}
tot_rev = 0.0
try:
    with open(input_file, 'r') as infile, \
         open(output_file, 'w') as outfile, \
         open(error_log, 'w') as errfile:
        for line_num, line in enumerate(infile, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 6:
                errfile.write(f"Line {line_num}: Malformed line -> {line}\n")
                continue
            else:
                try:
                    order_id = int(parts[0])
                    customer_name = parts[1]
                    product_id = parts[2]
                    product_name = parts[3]
                    quantity = int(parts[4])
                    unit_price = float(parts[5])
                    if quantity <= 0 or unit_price < 0.0:
                        raise ValueError("Invalid quantity or price!")
                    # aggregate valid orders
                    if product_name not in agg_data:
                        agg_data[product_name] = {
                            'product_id': None,
                            'order_id': [],
                            'customers': [],
                            'quantity': 0,
                            'sales': 0.0,
                            'price': 0
                        }
                        agg_data[product_name]['product_id'] = product_id
                        agg_data[product_name]['price'] = unit_price
                    agg_data[product_name]['order_id'].append(order_id)
                    agg_data[product_name]['customers'].append(customer_name)
                    agg_data[product_name]['quantity'] += quantity
                    agg_data[product_name]['sales'] += quantity * unit_price
                    tot_rev += quantity * unit_price
                except Exception as e:
                    errfile.write(f"Line {line_num}: {str(e)} -> {line}\n")
        # summary report
        outfile.write("SUMMARY REPORT\n")
        outfile.write("========================================\n")
        for prod, data in agg_data.items():
            outfile.write(
                f"\n{data['product_id']} - {prod}:\n"
                f" Order IDs: {data['order_id']}\n"
                f" Customers: {data['customers']}\n"
                f" Unit Price: Rs.{data['price']}\n"
                f" Total Quantity: {data['quantity']}\n"
                f" Sales: Rs.{data['sales']}\n"
            )
        outfile.write("\n")
        outfile.write(f"Total Revenue: Rs.{tot_rev}\n")
        outfile.write("========================================\n")
        print("Order Processed successfully. Check summary_report.txt and error_log.txt.")
except FileNotFoundError:
    print(f"Error: Input file not found at {input_file}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")