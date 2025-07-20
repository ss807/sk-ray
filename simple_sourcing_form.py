import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Simple SKU Sourcing",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .product-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .supplier-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sku_data():
    """Load SKU data from JSON file"""
    try:
        with open('final_sku.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data['products']
    except Exception as e:
        st.error(f"Error loading SKU data: {e}")
        return []

def save_sku_data(products):
    """Save SKU data to JSON file"""
    try:
        data = {
            "metadata": {
                "updated_timestamp": datetime.now().isoformat(),
                "total_products": len(products)
            },
            "products": products
        }
        with open('final_sku.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def load_sourcing_data():
    """Load sourcing data"""
    try:
        if os.path.exists('sourcing_data.json'):
            with open('sourcing_data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
    except Exception as e:
        st.warning(f"Could not load sourcing data: {e}")
    return {}

def save_sourcing_data(data):
    """Save sourcing data"""
    try:
        with open('sourcing_data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving sourcing data: {e}")
        return False

def add_log(action, details, product_name=None, supplier_name=None):
    """Add a log entry"""
    try:
        if os.path.exists('app_logs.json'):
            with open('app_logs.json', 'r', encoding='utf-8') as file:
                logs = json.load(file)
        else:
            logs = []
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "product_name": product_name,
            "supplier_name": supplier_name
        }
        
        logs.append(log_entry)
        
        # Keep only last 1000 logs
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        with open('app_logs.json', 'w', encoding='utf-8') as file:
            json.dump(logs, file, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error adding log: {e}")
        return False

def load_logs():
    """Load application logs"""
    try:
        if os.path.exists('app_logs.json'):
            with open('app_logs.json', 'r', encoding='utf-8') as file:
                return json.load(file)
    except Exception as e:
        st.warning(f"Could not load logs: {e}")
    return []

def main():
    st.markdown('<h1 class="main-header">📦 Simple SKU Sourcing</h1>', unsafe_allow_html=True)
    
    # Load data
    products = load_sku_data()
    sourcing_data = load_sourcing_data()
    
    if not products:
        st.error("No SKU data found. Please ensure 'final_sku.json' is in the current directory.")
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📋 Products", "💰 Sourcing", "📊 Logs"])
    
    with tab1:
        st.markdown("## 📋 Product Management")
        
        # Get unique categories
        categories = sorted(list(set(product.get('category_name', 'Uncategorized') for product in products)))
        
        # Category dropdown in main area
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_category = st.selectbox(
                "Select Category:",
                ["All Categories"] + categories,
                help="Choose a category to view products"
            )
        
        with col2:
            search_term = st.text_input("🔍 Search by Product Name:", "")
        
        # Filter products
        filtered_products = products
        if selected_category != "All Categories":
            filtered_products = [p for p in filtered_products if p.get('category_name', 'Uncategorized') == selected_category]
        
        if search_term:
            filtered_products = [p for p in filtered_products if search_term.lower() in p['product_name'].lower()]
        
        # Display category summary
        if selected_category == "All Categories":
            st.markdown(f"### 📦 All Products ({len(filtered_products)} total)")
            
            # Show category breakdown
            category_counts = {}
            for product in filtered_products:
                category = product.get('category_name', 'Uncategorized')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            col1, col2, col3, col4 = st.columns(4)
            for i, (category, count) in enumerate(sorted(category_counts.items())):
                if i < 4:
                    with [col1, col2, col3, col4][i]:
                        st.metric(category, count)
        else:
            st.markdown(f"### 📦 {selected_category} Products ({len(filtered_products)} products)")
        
        for product in filtered_products:
            with st.expander(f"📦 {product['product_name']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="product-card">
                        <strong>Product Index:</strong> {product['product_index']}<br>
                        <strong>Category:</strong> {product.get('category_name', 'Uncategorized')}<br>
                        <strong>Current Price:</strong> ₹{product.get('price_numeric', 'N/A')}<br>
                        <strong>Weight/Quantity:</strong> {product.get('weight_quantity', 'N/A')}<br>
                        <strong>Description:</strong> {product.get('description', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Count suppliers for this product
                    product_suppliers = sourcing_data.get(str(product['product_index']), [])
                    st.metric("Suppliers", len(product_suppliers))
                    
                    if product_suppliers:
                        st.write("**Current Suppliers:**")
                        for i, supplier in enumerate(product_suppliers):
                            st.write(f"• {supplier.get('supplier_name', 'Unknown')}")
                    else:
                        st.info("No suppliers added yet")
        
        # Add new product section
        st.markdown("---")
        st.markdown("### ➕ Add New Product")
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_product_name = st.text_input("Product Name:")
                new_category = st.selectbox("Category:", categories + ["New Category"])
                new_price = st.number_input("Price (₹):", min_value=0.0, value=0.0)
            
            with col2:
                new_weight = st.text_input("Weight/Quantity:")
                new_description = st.text_area("Description:")
                if new_category == "New Category":
                    new_category = st.text_input("Enter New Category Name:")
            
            if st.form_submit_button("Add Product"):
                if new_product_name and new_category:
                    # Find next product index
                    max_index = max(p['product_index'] for p in products) if products else 0
                    new_product = {
                        "product_index": max_index + 1,
                        "product_name": new_product_name,
                        "price_numeric": new_price,
                        "weight_quantity": new_weight,
                        "description": new_description,
                        "category_name": new_category
                    }
                    
                    products.append(new_product)
                    if save_sku_data(products):
                        add_log("Product Added", f"Added product '{new_product_name}' to category '{new_category}'", new_product_name)
                        st.success(f"Added new product: {new_product_name}")
                        st.rerun()
                else:
                    st.error("Please fill in product name and category")
    
    with tab2:
        st.markdown("## 💰 Sourcing Management")
        
        # Product selection
        st.markdown("### Select Product")
        
        # Group products by category for easier selection
        product_options = {}
        for product in products:
            category = product.get('category_name', 'Uncategorized')
            if category not in product_options:
                product_options[category] = []
            product_options[category].append(product)
        
        # Product selection dropdown
        selected_category_sourcing = st.selectbox("Category:", ["Select Category"] + list(product_options.keys()))
        
        if selected_category_sourcing != "Select Category":
            category_products = product_options[selected_category_sourcing]
            selected_product = st.selectbox(
                "Product:",
                category_products,
                format_func=lambda x: f"{x['product_index']}. {x['product_name']}"
            )
            
            if selected_product:
                product_index = selected_product['product_index']
                
                # Show product info
                st.markdown(f"""
                <div class="product-card">
                    <strong>Selected Product:</strong> {selected_product['product_name']}<br>
                    <strong>Category:</strong> {selected_product.get('category_name', 'Uncategorized')}<br>
                    <strong>Current Price:</strong> ₹{selected_product.get('price_numeric', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
                
                # Show existing suppliers
                existing_suppliers = sourcing_data.get(str(product_index), [])
                if existing_suppliers:
                    st.markdown("### 📋 Existing Suppliers")
                    for i, supplier in enumerate(existing_suppliers):
                        with st.expander(f"🏢 {supplier.get('supplier_name', 'Unknown')}", expanded=False):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Contact:** {supplier.get('contact_info', 'N/A')}")
                                st.write(f"**Delivery Time:** {supplier.get('delivery_time', 'N/A')} days")
                                st.write(f"**MOQ:** {supplier.get('moq', 'N/A')}")
                            with col2:
                                st.write("**Quantity Pricing:**")
                                for tier, price in supplier.get('quantity_pricing', {}).items():
                                    st.write(f"• {tier} units: ₹{price}")
                
                # Add new supplier
                st.markdown("### ➕ Add New Supplier")
                
                with st.form("add_supplier_form"):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        supplier_name = st.text_input("Supplier Name:")
                        contact_info = st.text_input("Contact Info:")
                        delivery_time = st.number_input("Delivery Time (days):", min_value=1, value=7)
                        moq = st.number_input("Minimum Order Quantity:", min_value=1, value=10)
                    
                    with col2:
                        st.markdown("**Quantity-Based Pricing (3 slabs):**")
                        
                        # Slab 1
                        qty1_min = st.number_input("Slab 1 - Min Qty:", min_value=1, value=1)
                        qty1_price = st.number_input("Slab 1 - Price (₹):", min_value=0.0, value=0.0)
                        
                        # Slab 2
                        qty2_min = st.number_input("Slab 2 - Min Qty:", min_value=1, value=10)
                        qty2_price = st.number_input("Slab 2 - Price (₹):", min_value=0.0, value=0.0)
                        
                        # Slab 3
                        qty3_min = st.number_input("Slab 3 - Min Qty:", min_value=1, value=50)
                        qty3_price = st.number_input("Slab 3 - Price (₹):", min_value=0.0, value=0.0)
                    
                    if st.form_submit_button("Add Supplier"):
                        # Validate quantity slabs
                        if qty1_min >= qty2_min or qty2_min >= qty3_min:
                            st.error("Quantity slabs should be in ascending order (e.g., 1, 10, 50)")
                        elif supplier_name:
                            new_supplier = {
                                "supplier_name": supplier_name,
                                "contact_info": contact_info,
                                "delivery_time": delivery_time,
                                "moq": moq,
                                "quantity_pricing": {
                                    f"{qty1_min}+": qty1_price,
                                    f"{qty2_min}+": qty2_price,
                                    f"{qty3_min}+": qty3_price
                                },
                                "added_date": datetime.now().isoformat()
                            }
                            
                            # Add to existing suppliers or create new list
                            if str(product_index) not in sourcing_data:
                                sourcing_data[str(product_index)] = []
                            
                            sourcing_data[str(product_index)].append(new_supplier)
                            
                            if save_sourcing_data(sourcing_data):
                                add_log("Supplier Added", f"Added supplier '{supplier_name}' for product '{selected_product['product_name']}'", selected_product['product_name'], supplier_name)
                                st.success(f"Added supplier: {supplier_name}")
                                st.rerun()
                        else:
                            st.error("Please enter supplier name")
        
        # Export section
        st.markdown("---")
        st.markdown("### 📊 Export Data")
        
        if st.button("📄 Export Sourcing Data"):
            if sourcing_data:
                # Create export DataFrame
                export_data = []
                for product_index, suppliers in sourcing_data.items():
                    product = next((p for p in products if p['product_index'] == int(product_index)), None)
                    if product:
                        for supplier in suppliers:
                            for tier, price in supplier.get('quantity_pricing', {}).items():
                                export_data.append({
                                    'Product Index': product_index,
                                    'Product Name': product['product_name'],
                                    'Category': product.get('category_name', 'Uncategorized'),
                                    'Supplier Name': supplier.get('supplier_name', ''),
                                    'Contact Info': supplier.get('contact_info', ''),
                                    'Delivery Time': supplier.get('delivery_time', ''),
                                    'MOQ': supplier.get('moq', ''),
                                    'Min Quantity': tier,
                                    'Price': price
                                })
                
                if export_data:
                    df = pd.DataFrame(export_data)
                    df.to_excel('sourcing_export.xlsx', index=False)
                    st.success("Exported to 'sourcing_export.xlsx'")
                else:
                    st.warning("No data to export")
            else:
                st.warning("No sourcing data available")
    
    with tab3:
        st.markdown("## 📊 Application Logs")
        
        # Load logs
        logs = load_logs()
        
        if not logs:
            st.info("No logs available yet. Start using the application to see activity logs.")
        else:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Action filter
                actions = sorted(list(set(log.get('action', '') for log in logs)))
                selected_action = st.selectbox("Filter by Action:", ["All Actions"] + actions)
            
            with col2:
                # Date filter
                from datetime import datetime, timedelta
                today = datetime.now().date()
                date_filter = st.selectbox("Filter by Date:", 
                    ["All Time", "Today", "Last 7 Days", "Last 30 Days"])
            
            with col3:
                # Search
                search_log = st.text_input("🔍 Search in logs:", "")
            
            # Filter logs
            filtered_logs = logs
            
            if selected_action != "All Actions":
                filtered_logs = [log for log in filtered_logs if log.get('action') == selected_action]
            
            if date_filter != "All Time":
                cutoff_date = None
                if date_filter == "Today":
                    cutoff_date = today
                elif date_filter == "Last 7 Days":
                    cutoff_date = today - timedelta(days=7)
                elif date_filter == "Last 30 Days":
                    cutoff_date = today - timedelta(days=30)
                
                if cutoff_date:
                    filtered_logs = [log for log in filtered_logs 
                                   if datetime.fromisoformat(log['timestamp'].split('T')[0]).date() >= cutoff_date]
            
            if search_log:
                filtered_logs = [log for log in filtered_logs 
                               if search_log.lower() in log.get('details', '').lower() 
                               or search_log.lower() in log.get('product_name', '').lower()
                               or search_log.lower() in log.get('supplier_name', '').lower()]
            
            # Display logs
            st.markdown(f"### Showing {len(filtered_logs)} log entries")
            
            # Export logs
            if st.button("📄 Export Logs"):
                if filtered_logs:
                    df = pd.DataFrame(filtered_logs)
                    df.to_excel('application_logs.xlsx', index=False)
                    st.success("Exported logs to 'application_logs.xlsx'")
                else:
                    st.warning("No logs to export")
            
            # Display logs in reverse chronological order
            for log in reversed(filtered_logs):
                timestamp = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                with st.expander(f"🕒 {formatted_time} - {log.get('action', 'Unknown Action')}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Details:** {log.get('details', 'No details')}")
                        if log.get('product_name'):
                            st.write(f"**Product:** {log.get('product_name')}")
                        if log.get('supplier_name'):
                            st.write(f"**Supplier:** {log.get('supplier_name')}")
                    
                    with col2:
                        st.write(f"**Action:** {log.get('action', 'Unknown')}")
                        st.write(f"**Time:** {formatted_time}")

if __name__ == "__main__":
    main() 