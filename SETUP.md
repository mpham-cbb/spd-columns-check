# Setup Guide for Column Validator

## Environment Variables Setup

### Method 1: Using .env file (Recommended for Development)

1. Copy the template file:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file with your credentials:
   ```
   VALIDATOR_USERNAME=your_username
   VALIDATOR_PASSWORD=your_secure_password
   STREAMLIT_ENV=development
   ```

3. The `.env` file will be automatically loaded when the app starts.

### Method 2: System Environment Variables (Recommended for Production)

#### Windows:
```cmd
set VALIDATOR_USERNAME=your_username
set VALIDATOR_PASSWORD=your_secure_password
set STREAMLIT_ENV=production
```

#### Linux/Mac:
```bash
export VALIDATOR_USERNAME=your_username
export VALIDATOR_PASSWORD=your_secure_password
export STREAMLIT_ENV=production
```

#### For permanent setup, add to your system's environment variables or shell profile.

### Method 3: Cloud Deployment Environment Variables

When deploying to cloud platforms (Heroku, Streamlit Cloud, etc.), set these environment variables in your deployment platform's settings:

- `VALIDATOR_USERNAME`: Your chosen username
- `VALIDATOR_PASSWORD`: Your secure password
- `STREAMLIT_ENV`: Set to `production`

## File Naming Requirements (CASE SENSITIVE)

### For ABC, SRS, QXO customers:
- **MASTIC files**: Must start with `NET_ASP_MASTIC` (exact case)
- **VARIFORM files**: Must start with `NET_ASP_VF` (exact case)

### For NVR, WW customers:
- **All files**: Must start with `NET_ASP` (exact case)
- No product line selection required

## Examples:
✅ **Valid filenames:**
- `NET_ASP_MASTIC_2024_Q1.xlsx`
- `NET_ASP_VF_Report.csv`
- `NET_ASP_Data_Export.xlsx` (for NVR/WW)

❌ **Invalid filenames:**
- `net_asp_mastic_data.xlsx` (lowercase)
- `NET_ASP_Mastic_Report.csv` (mixed case)
- `Data_NET_ASP_MASTIC.xlsx` (doesn't start with pattern)

## Security Notes

1. **Never commit `.env` files** to version control
2. Use strong passwords for production
3. Change default credentials before deployment
4. Consider using more sophisticated authentication for production use
