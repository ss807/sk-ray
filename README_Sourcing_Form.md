# 💰 SKU Sourcing Cost Form

A comprehensive web application built with Streamlit to manage sourcing costs for your SKU inventory. This application provides a user-friendly interface similar to Google Forms for entering detailed sourcing information including quantity-based pricing, platform considerations, and supplier details.

## 🚀 Features

### 📦 Core Functionality
- **Product Management**: Load and manage 161+ SKUs from your `final_sku.json` file
- **Quantity-Based Pricing**: Set different costs for different order quantities (1-10, 11-50, 51-100, 101-500, 500+)
- **Platform Support**: Track sourcing from multiple platforms (Swiggy, Zomato, Amazon, Flipkart, Direct Supplier, etc.)
- **Supplier Management**: Record supplier names, lead times, and quality ratings

### 🎯 Advanced Features
- **Batch Processing**: Fill common details for multiple products at once
- **Progress Tracking**: Visual progress indicator showing completion status
- **Search & Filter**: Filter products by category and search by product name
- **Data Persistence**: Save progress automatically and continue later
- **Export Options**: Export data to Excel with detailed reports

### 📊 Analytics & Reporting
- **Real-time Calculations**: Automatic selling price calculation based on cost and margin
- **Summary Reports**: Generate comprehensive sourcing cost summaries
- **Data Preview**: View all entered data in a clean table format
- **Quality Ratings**: Track supplier quality (Excellent, Good, Average, Poor)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Your `final_sku.json` file in the same directory

### Installation Steps

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run sourcing_cost_form.py
   ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:8501`
   - The application will automatically load your SKU data

## 📋 How to Use

### 1. Getting Started
- The application loads your SKU data automatically from `final_sku.json`
- Use the sidebar to filter products by category or search by product name
- Navigate between tabs: "Product Costs", "Summary & Export", and "Settings"

### 2. Entering Sourcing Costs

#### Individual Product Entry:
1. Click on the expandable product cards in the "Product Costs" tab
2. Fill in the following details:
   - **Platform**: Select the sourcing platform
   - **Supplier Name**: Enter the supplier's name
   - **Lead Time**: Number of days for delivery
   - **Minimum Order Quantity**: Minimum units required
   - **Shipping Cost**: Additional shipping charges
   - **Quality Rating**: Rate the supplier quality

#### Quantity-Based Pricing:
For each quantity tier (1-10, 11-50, 51-100, 101-500, 500+):
- **Cost**: Enter the sourcing cost per unit
- **Margin %**: Set your desired profit margin
- **Selling Price**: Automatically calculated
- **Notes**: Add any specific notes for that tier

#### Batch Processing:
1. Enable "Batch Mode" checkbox
2. Select multiple products from the dropdown
3. Fill in common details once
4. Click "Apply to Selected Products" to apply to all selected items

### 3. Saving & Exporting Data

#### Save Progress:
- Click "💾 Save All Data" in the "Summary & Export" tab
- Data is saved to `sourcing_costs.json` for future use

#### Export Options:
- **📄 Export to Excel**: Creates detailed Excel file with all data
- **📊 Export Summary Report**: Creates a summary report with best pricing tiers

### 4. Data Management

#### Settings Tab:
- **Reset All Data**: Clear all entered data
- **Load Backup**: Upload a backup JSON file
- **Custom Settings**: Modify quantity tiers and platforms

## 📁 File Structure

```
vibizo/
├── final_sku.json              # Your original SKU data
├── sourcing_cost_form.py       # Main application
├── requirements.txt            # Python dependencies
├── README_Sourcing_Form.md     # This file
├── sourcing_costs.json         # Generated: Your entered data
├── sourcing_costs_export.xlsx  # Generated: Detailed export
└── sourcing_summary_report.xlsx # Generated: Summary report
```

## 🔧 Customization

### Modifying Quantity Tiers
1. Go to the "Settings" tab
2. Edit the "Custom Quantity Tiers" text area
3. Enter tiers in format: "1-10", "11-50", etc.
4. Save settings

### Adding New Platforms
1. Go to the "Settings" tab
2. Edit the "Custom Platforms" text area
3. Add new platform names (one per line)
4. Save settings

## 💡 Best Practices

### Data Entry Tips:
1. **Start with Batch Mode**: Use batch processing for products with similar suppliers
2. **Use Search & Filter**: Filter by category to focus on specific product types
3. **Save Regularly**: Save your progress frequently to avoid data loss
4. **Add Notes**: Use the notes field to record important supplier information

### Cost Management:
1. **Compare Platforms**: Enter costs from multiple platforms for comparison
2. **Track Quality**: Use quality ratings to identify reliable suppliers
3. **Monitor Lead Times**: Consider lead times when planning inventory
4. **Review Margins**: Ensure your margins are competitive and profitable

## 🚨 Troubleshooting

### Common Issues:

1. **"No SKU data found"**:
   - Ensure `final_sku.json` is in the same directory as the application
   - Check that the JSON file is properly formatted

2. **Application won't start**:
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **Data not saving**:
   - Check file permissions in the directory
   - Ensure there's enough disk space

4. **Export not working**:
   - Make sure you have data entered before exporting
   - Check that Excel files aren't open in another application

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your `final_sku.json` file format
3. Ensure all dependencies are properly installed

## 🔄 Updates & Maintenance

The application automatically:
- Loads your existing data when restarted
- Tracks when data was last updated
- Provides backup and restore functionality
- Maintains data integrity across sessions

---

**Happy Sourcing! 🎯** 