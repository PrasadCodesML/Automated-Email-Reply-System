from typing import Dict, Any, Optional, List
import mysql.connector
import re
from datetime import datetime


def get_database_connection(database_name: str = "TE_Email_Custom_Database"):
    """Establish and return a database connection."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database=database_name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return None


def format_response(data: Dict[str, Any], template: str) -> str:
    """Format data using the provided template."""
    response = f"📅 **Date:** {datetime.now().strftime('%B %d, %Y')}\n\n"
    response += template.format(**data)
    response += "\n\n**Best Regards,**  \nTE Connectivity Support Team"
    return response


def extract_id(query: str, pattern: str, error_message: str) -> Optional[str]:
    """Extract ID from query using the provided pattern."""
    id_match = re.search(pattern, query)
    if not id_match:
        return None
    return id_match.group(1).upper()


def process_pos_replacement_query(query: str) -> str:
    """Process POS replacement queries."""
    quote_id = extract_id(query, r'QTID(\d{1,3})', "Could not find a valid Quote ID in the query.")
    if not quote_id:
        return " Could not find a valid Quote ID in the query. Please provide a 10-digit Quote ID."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 01_pos_replacemnt WHERE quote_id = %s"""
        cursor.execute(query_sql, (quote_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for Quote ID: {quote_id}**

Possible reasons:
- The quote may not exist in our database
- The quote ID format might be incorrect

Please verify the quote ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        template = """
🔹 **Quote ID:** {quote_id}  
🔹 **Current POS Customer:** {current_pos_customer}  
🔹 **New POS Customer:** {new_pos_customer}  
🔹 **Conflict Found:** {conflict_found}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  
"""
        
        # Ensure all fields exist
        data = {
            "quote_id": quote_id,
            "current_pos_customer": result.get("current_pos_customer", "N/A"),
            "new_pos_customer": result.get("new_pos_customer", "N/A"),
            "conflict_found": result.get("conflict_found", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_general_pricing_query(query: str) -> str:
    """Process general pricing queries."""
    quote_id = extract_id(query, r'QTID(\d{1,3})', "Could not find a valid Quote ID in the query.")
    if not quote_id:
        return " Could not find a valid Quote ID in the query. Please provide a 10-digit Quote ID."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 02_general_pricing_queries WHERE quote_id = %s"""
        cursor.execute(query_sql, (quote_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No pricing information found for Quote ID: {quote_id}**

Possible reasons:
- The quote may not exist in our database
- The quote ID format might be incorrect

Please verify the quote ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Check if closed by BUPA
        closed_by = result.get("closed_by", "").lower()
        is_bupa_closed = closed_by and ("bupa" in closed_by or "business partner" in closed_by)
        
        if is_bupa_closed:
            template = """
🔹 **Quote ID:** {quote_id}  
🔹 **Query Type:** {query_type}  
🔹 **Quote Status:** {quote_status}  

 **This quote has been closed by BUPA.**  

**Next Steps:**  
{next_action_required}  

🔗 Please direct further queries to **BUPA** for more information.  
"""
        else:
            template = """
🔹 **Quote ID:** {quote_id}  
🔹 **Query Type:** {query_type}  
🔹 **Quote Status:** {quote_status}  
🔹 **Closed By:** {closed_by}  

**Next Steps:**  
{next_action_required}  
"""
        
        data = {
            "quote_id": quote_id,
            "query_type": result.get("query_type", "N/A"),
            "quote_status": result.get("quote_status", "N/A"),
            "closed_by": result.get("closed_by", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_piggyback_creation_query(query: str) -> str:
    """Process piggyback creation queries."""
    # Extract request ID (format can vary, so using a generic pattern)
    print(query)
    request_id = extract_id(query, r'(PBK\d+|P\d+|REQ\d+)', "Could not find a valid Request ID in the query.")
    print(request_id)
    
    if not request_id:
        return " Could not find a valid Request ID in the query. Please provide a valid Request ID (format: P##### or REQ#####)."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 03_piggyback_creation_queries WHERE request_id = %s"""
        cursor.execute(query_sql, (request_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for Request ID: {request_id}**

Possible reasons:
- The request may not exist in our database
- The request ID format might be incorrect

Please verify the request ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        template = """
🔹 **Request ID:** {request_id}  
🔹 **Distributor:** {distributor_name}  
🔹 **OEM Agreement ID:** {oem_agreement_id}  
🔹 **Part Numbers Involved:** {part_numbers_involved}  
🔹 **Additional Uplift Required:** {additional_uplift_required}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  
"""
        
        data = {
            "request_id": result.get("request_id", "N/A"),
            "distributor_name": result.get("distributor_name", "N/A"),
            "oem_agreement_id": result.get("oem_agreement_id", "N/A"),
            "part_numbers_involved": result.get("part_numbers_involved", "N/A"),
            "additional_uplift_required": result.get("additional_uplift_required", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_adding_parts_to_piggyback_query(query: str) -> str:
    """Process queries for adding parts to existing piggyback."""
    # Try to extract piggyback ID
    piggyback_id = extract_id(query, r'(ADD\d+|PGB-\d+)', "Could not find a valid Piggyback ID in the query.")
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # First, get the structure of the table
        cursor.execute("DESCRIBE 04_adding_parts_pos_queries")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        if piggyback_id:
            # Try to find columns that might contain the piggyback ID
            piggyback_columns = [col for col in column_names if "pgb" in col.lower() or "pig" in col.lower()]
            
            if piggyback_columns:
                # Create a query that searches for the piggyback ID in any of these columns
                conditions = []
                params = []
                for col in piggyback_columns:
                    conditions.append(f"{col} LIKE %s")
                    params.append(f"%{piggyback_id}%")
                
                query_sql = f"""SELECT * FROM 04_adding_parts_pos_queries WHERE {" OR ".join(conditions)}"""
                cursor.execute(query_sql, params)
            else:
                # If no piggyback-specific columns, search in all columns
                query_sql = "SELECT * FROM 04_adding_parts_pos_queries LIMIT 1"
                cursor.execute(query_sql)
        else:
            # Without a piggyback ID, just fetch the most recent record
            query_sql = "SELECT * FROM 04_adding_parts_pos_queries LIMIT 1"
            cursor.execute(query_sql)
        
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for Piggyback ID: {piggyback_id or 'Unknown'}**

Possible reasons:
- The request may not exist in our database
- The piggyback ID format might be incorrect

Please verify the piggyback ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Build response based on available columns
        template = """
🔹 **Request ID:** {add88632}  
🔹 **Piggyback ID:** {pgb}  
🔹 **Distributor:** {distributor}  
🔹 **Part Number(s):** {pn}  
🔹 **POS Customer:** {pos}  
🔹 **Status:** {status}  

**Next Steps:**  
{next_action}  

**Additional Information:** {additional_info}  
"""
        
        data = {
            "add88632": result.get("add88632", "N/A"),
            "pgb": result.get("pgb-4023", "N/A"),
            "distributor": result.get("distributor_m_ltd", "N/A"),
            "pn": result.get("pn-515629", "N/A"),
            "pos": result.get("pos-customer_w_inc", "N/A"),
            "status": "Rejected" if result.get("rejected") == "Yes" else "Processing",
            "next_action": result.get("approve_and_update_database", "Review request."),
            "additional_info": "Duplicate request detected." if result.get("duplicate_request_detected") == "Yes" else "N/A"
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_ship_debit_query(query: str) -> str:
    """Process ship and debit queries."""
    quote_id = extract_id(query, r'QTID(\d{1,13})', "Could not find a valid Quote ID in the query.")
    print(quote_id)
    if not quote_id:
        return " Could not find a valid Quote ID in the query. Please provide a 10-digit Quote ID."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 05_ship_debit_queries WHERE quote_id = %s"""
        cursor.execute(query_sql, (quote_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No ship and debit information found for Quote ID: {quote_id}**

Possible reasons:
- The quote may not exist in our database
- The quote ID format might be incorrect

Please verify the quote ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Check if closed by BUPA
        closed_by = result.get("quote_closed_by", "").lower()
        is_bupa_closed = closed_by and ("bupa" in closed_by or "business partner" in closed_by)
        
        if is_bupa_closed:
            template = """
🔹 **Quote ID:** {quote_id}  
🔹 **FSA to S&D Conversion:** {fsa_to_sandd_conversion}  
🔹 **POS Customer:** {pos_customer}  
🔹 **End Customer:** {end_customer}  
🔹 **Address Issue:** {address_issue}  

 **This quote has been closed by BUPA.**  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  

🔗 Please direct further queries to **BUPA** for more information.  
"""
        else:
            template = """
🔹 **Quote ID:** {quote_id}  
🔹 **FSA to S&D Conversion:** {fsa_to_sandd_conversion}  
🔹 **POS Customer:** {pos_customer}  
🔹 **End Customer:** {end_customer}  
🔹 **Address Issue:** {address_issue}  
🔹 **Quote Closed By:** {quote_closed_by}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  
"""
        
        data = {
            "quote_id": quote_id,
            "fsa_to_sandd_conversion": result.get("fsa_to_sandd_conversion", "N/A"),
            "pos_customer": result.get("pos_customer", "N/A"),
            "end_customer": result.get("end_customer", "N/A"),
            "address_issue": result.get("address_issue", "N/A"),
            "quote_closed_by": result.get("quote_closed_by", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_opportunities_rejected_sfdc_query(query: str) -> str:
    """Process queries about rejected opportunities in SFDC."""
    opportunity_id = extract_id(query, r'#?(\d{9})', "Could not find a valid Opportunity ID in the query.")
    if not opportunity_id:
        return " Could not find a valid Opportunity ID in the query. Please provide a 9-digit Opportunity ID."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 06_sfdc_rejection_queries WHERE opportunity_id = %s"""
        cursor.execute(query_sql, (opportunity_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for Opportunity ID: {opportunity_id}**

Possible reasons:
- The opportunity may not exist in our database
- The opportunity ID format might be incorrect

Please verify the opportunity ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Check if rejected by DMM
        rejected_by = result.get("rejected_by", "").lower()
        is_dmm_rejected = rejected_by and "dmm" in rejected_by
        
        if is_dmm_rejected:
            template = """
🔹 **Opportunity ID:** {opportunity_id}  
🔹 **Rejection Reason:** {rejection_reason}  

 **This opportunity has been rejected by DMM.**  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  

🔗 Please direct further queries to **DMM** for more information.  
"""
        else:
            template = """
🔹 **Opportunity ID:** {opportunity_id}  
🔹 **Rejection Reason:** {rejection_reason}  
🔹 **Rejected By:** {rejected_by}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  
"""
        
        data = {
            "opportunity_id": opportunity_id,
            "rejection_reason": result.get("rejection_reason", "N/A"),
            "rejected_by": result.get("rejected_by", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_pending_approval_sfdc_query(query: str) -> str:
    """Process queries about opportunities pending approval in SFDC."""
    opportunity_id = extract_id(query, r'#?(\d{9})', "Could not find a valid Opportunity ID in the query.")
    if not opportunity_id:
        return " Could not find a valid Opportunity ID in the query. Please provide a 9-digit Opportunity ID."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 07_sfdc_pendingapproval_queries WHERE opportunity_id = %s"""
        cursor.execute(query_sql, (opportunity_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No pending approval information found for Opportunity ID: {opportunity_id}**

Possible reasons:
- The opportunity may not exist in our database
- The opportunity ID format might be incorrect
- The opportunity might not be in pending approval status

Please verify the opportunity ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        template = """
🔹 **Opportunity ID:** {opportunity_id}  
🔹 **Pending With:** {pending_with}  
🔹 **Approval Status:** {approval_status}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  

🔗 This opportunity is currently pending with DMM for approval. DMM has been notified to review and approve.
"""
        
        data = {
            "opportunity_id": opportunity_id,
            "pending_with": result.get("pending_with", "N/A"),
            "approval_status": result.get("approval_status", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_quote_closed_gpms_no_document_query(query: str) -> str:
    """Process queries for quotes closed in GPMS but no document available."""
    quote_id = extract_id(query, r'#?(\d{10})', "Could not find a valid Quote ID in the query.")
    if not quote_id:
        return " Could not find a valid Quote ID in the query. Please provide a 10-digit Quote ID."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 08_cases_where_gpms WHERE quote_id = %s"""
        cursor.execute(query_sql, (quote_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for Quote ID: {quote_id}**

Possible reasons:
- The quote may not exist in our database
- The quote ID format might be incorrect

Please verify the quote ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        template = """
🔹 **Quote ID:** {quote_id}  
🔹 **Issue Type:** {issue_type}  
🔹 **System Affected:** {system_affected}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  

🛠️ A TEIS ticket has been created to re-trigger the quote to SAP. You will be notified once the document is available.
"""
        
        data = {
            "quote_id": quote_id,
            "issue_type": result.get("issue_type", "Document Not Available"),
            "system_affected": result.get("system_affected", "GPMS -> SAP"),
            "next_action_required": result.get("next_action_required", "TEIS ticket created to re-trigger the quote."),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_quote_not_reaching_pricing_query(query: str) -> str:
    """Process queries for quotes not reaching pricing."""
    quote_id = extract_id(query, r'#?(\d{10})', "Could not find a valid Quote ID in the query.")
    if not quote_id:
        return " Could not find a valid Quote ID in the query. Please provide a 10-digit Quote ID."
    
    connection = get_database_connection()
    if not connection:
        return " Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        query_sql = """SELECT * FROM 09_gpms_sfdc WHERE quote_id = %s"""
        cursor.execute(query_sql, (quote_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for Quote ID: {quote_id}**

Possible reasons:
- The quote may not exist in our database
- The quote ID format might be incorrect

Please verify the quote ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        template = """
🔹 **Quote ID:** {quote_id}  
🔹 **Issue Type:** {issue_type}  
🔹 **System Affected:** {system_affected}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  

🛠️ A TEIS ticket has been created to re-trigger the quote from SAP and remove any pricing blocks.
"""
        
        data = {
            "quote_id": quote_id,
            "issue_type": result.get("issue_type", "Quote Not Reaching Pricing"),
            "system_affected": result.get("system_affected", "SAP -> GPMS/SFDC"),
            "next_action_required": result.get("next_action_required", "TEIS ticket created to investigate."),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f" Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def process_customer_data_enquiries_query(query: str) -> str:
    """Process customer data enquiries."""
    # Extract request ID for customer data enquiries
    request_id = extract_id(query, r'(REQ\d+|CUST\d+|CDE\d+)', "Could not find a valid Customer Data Request ID in the query.")
    
    if not request_id:
        return "⚠️ Could not find a valid Customer Data Request ID in the query. Please provide a valid Request ID."
    
    connection = get_database_connection()
    if not connection:
        return "⚠️ Unable to connect to the database. Please try again later."
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query_sql = """SELECT * FROM 10_customer_data_enquiries WHERE request_id = %s"""
        cursor.execute(query_sql, (request_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for Request ID: {request_id}**

Possible reasons:
- The request may not exist in our database
- The request ID format might be incorrect

Please verify the request ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        template = """
🔹 **Request ID:** {request_id}  
🔹 **Requested By:** {requested_by}  
🔹 **Data Type Requested:** {data_type_requested}  
🔹 **Verification Status:** {verification_status}  

**Next Steps:**  
{next_action_required}  

**Additional Information:** {additional_findings}  
"""
        
        data = {
            "request_id": result.get("request_id", "N/A"),
            "requested_by": result.get("requested_by", "N/A"),
            "data_type_requested": result.get("data_type_requested", "N/A"),
            "verification_status": result.get("verification_status", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        return format_response(data, template)
    
    except mysql.connector.Error as err:
        return f"⚠️ Database Error: {err}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def process_gpms_pending_quotes(query):
    """Process queries about quotes pending for review on GPMS (Type 11)."""
    print(f"🔍 Processing GPMS pending quotes query: {query}")
    
    quote_id = extract_id(query, r'#?(\d{10})', "Could not find a valid Quote ID in the query.")
    if not quote_id:
        return " Could not find a valid Quote ID in the query. Please provide a **10-digit** Quote ID."
    
    print(f"📝 Extracted Quote ID: {quote_id}")
    
    try:
        conn = get_database_connection()
        if not conn:
            return " Database connection error. Please try again later."
        
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM 11_gpms_pending_quotes_queries WHERE quote_id = %s"""
        cursor.execute(query, (quote_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

 **No information found for Quote ID: {quote_id}**

Possible reasons:
- The quote may not exist in our database
- The quote ID format might be incorrect

Please verify the quote ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Format the data for the response
        data = {
            "quote_id": quote_id,
            "pending_with": result.get("pending_with", "N/A"),
            "review_status": result.get("review_status", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        # Check if quote is pending with BUPA
        is_bupa_pending = False
        pending_with = data["pending_with"].lower()
        if "bupa" in pending_with or "business partner" in pending_with:
            is_bupa_pending = True
            print("🔍 Identified as BUPA-pending quote")
        
        template = """
📅 **Date:** {current_date}

🔹 **Quote ID:** {quote_id}  
🔹 **Pending With:** {pending_with}  
🔹 **Review Status:** {review_status}  

"""
        
        if is_bupa_pending:
            template += """ **This quote is pending with BUPA.**  

**Next Steps:**  
 {next_action_required}  
 **Additional Findings:** {additional_findings}  

 🔗 Please direct further queries to **BUPA** for more information.  
"""
        else:
            template += """**Next Steps:**  
{next_action_required}  
**Additional Findings:** {additional_findings}  

🔗 Please let us know if you need any further assistance.  
"""
        
        template += """
**Best Regards,**  
TE Connectivity Support Team
"""
        
        return format_response(data, template)
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return f" Database error occurred while processing your request: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")

def process_sfdc_pending_opportunities(query):
    """Process queries about opportunities pending for review on SFDC (Type 12)."""
    print(f"🔍 Processing SFDC pending opportunities query: {query}")
    
    quote_id = extract_id(query, r'#?(\d{10})', "Could not find a valid Quote ID in the query.")
    # Extract opportunity ID - add this line after the quote_id extraction
    opportunity_id = extract_id(query, r'opportunity\s+(?:id|#)?\s*[:=]?\s*(\d{9})', "Could not find a valid Opportunity ID in the query.")
    if not opportunity_id:
        return " Could not find a valid Opportunity ID in the query. Please provide a **9-digit** Opportunity ID."
    
    print(f"📝 Extracted Opportunity ID: {opportunity_id}")
    
    try:
        conn = get_database_connection()
        if not conn:
            return " Database connection error. Please try again later."
        
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM 12_sfdc_pending_opp_queries WHERE opportunity_id = %s"""
        cursor.execute(query, (opportunity_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

 **No information found for Opportunity ID: {opportunity_id}**

Possible reasons:
- The opportunity may not exist in our database
- The opportunity ID format might be incorrect

Please verify the opportunity ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Format the data for the response
        data = {
            "opportunity_id": opportunity_id,
            "pending_with": result.get("pending_with", "N/A"),
            "review_status": result.get("review_status", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        template = """
📅 **Date:** {current_date}

🔹 **Opportunity ID:** {opportunity_id}  
🔹 **Pending With:** {pending_with}  
🔹 **Review Status:** {review_status}  

Could you please approve the opportunity #{opportunity_id} pending with you for review on SFDC and push it to pricing.

**Next Steps:**  
{next_action_required}  
**Additional Findings:** {additional_findings}  

🔗 Please let us know if you need any further assistance.  

**Best Regards,**  
TE Connectivity Support Team
"""
        
        return format_response(data, template)
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return f" Database error occurred while processing your request: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")

def process_opportunity_rejected_incorrectly(query):
    """Process queries about opportunities incorrectly rejected on SFDC (Type 13)."""
    print(f"🔍 Processing incorrectly rejected opportunity query: {query}")
    
    quote_id = extract_id(query, r'#?(\d{10})', "Could not find a valid Quote ID in the query.")
    # Extract opportunity ID - add this line after the quote_id extraction
    opportunity_id = extract_id(query, r'opportunity\s+(?:id|#)?\s*[:=]?\s*(\d{9})', "Could not find a valid Opportunity ID in the query.")
    if not opportunity_id:
        return " Could not find a valid Opportunity ID in the query. Please provide a **9-digit** Opportunity ID."
    
    print(f"📝 Extracted Opportunity ID: {opportunity_id}")
    
    try:
        conn = get_database_connection()
        if not conn:
            return " Database connection error. Please try again later."
        
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM 13_reply_to_requestor WHERE opportunity_id = %s"""
        cursor.execute(query, (opportunity_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

 **No information found for Opportunity ID: {opportunity_id}**

Possible reasons:
- The opportunity may not exist in our database
- The opportunity ID format might be incorrect

Please verify the opportunity ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Format the data for the response
        data = {
            "opportunity_id": opportunity_id,
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        template = """
📅 **Date:** {current_date}

🔹 **Opportunity ID:** {opportunity_id}  

The opportunity #{opportunity_id} has been rejected on SFDC and unfortunately this cannot be revoked, kindly ask the customer to raise another new opportunity with correct customer chain and share with us the reference number immediately to avoid potential rejections again.

**Next Steps:**  
{next_action_required}  
**Additional Findings:** {additional_findings}  

**Best Regards,**  
TE Connectivity Support Team
"""
        
        return format_response(data, template)
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return f" Database error occurred while processing your request: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")

def process_loa_related_queries(query):
    """Process LOA (Letter of Authorization) related queries (Type 14)."""
    print(f"🔍 Processing LOA related query: {query}")
    
    loa_request_id = extract_id(query, r'#?(\d{10})', "Could not find a valid Quote ID in the query.")
    if not loa_request_id:
        return " Could not find a valid LOA Request ID in the query. Please provide the LOA Request ID."
    
    print(f"📝 Extracted LOA Request ID: {loa_request_id}")
    
    try:
        conn = get_database_connection()
        if not conn:
            return " Database connection error. Please try again later."
        
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM 14_loa_queries WHERE loa_request_id = %s"""
        cursor.execute(query, (loa_request_id,))
        result = cursor.fetchone()
        
        if not result:
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

 **No information found for LOA Request ID: {loa_request_id}**

Possible reasons:
- The LOA request may not exist in our database
- The LOA request ID format might be incorrect

Please verify the LOA request ID and try again.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        # Format the data for the response
        data = {
            "loa_request_id": loa_request_id,
            "received_from": result.get("received_from", "N/A"),
            "loa_verification_status": result.get("loa_verification_status", "N/A"),
            "next_action_required": result.get("next_action_required", "N/A"),
            "additional_findings": result.get("additional_findings", "N/A")
        }
        
        # Check if LOA is correct or incorrect
        loa_status = data["loa_verification_status"].lower()
        is_loa_correct = "correct" in loa_status or "valid" in loa_status
        
        template = """
📅 **Date:** {current_date}

🔹 **LOA Request ID:** {loa_request_id}  
🔹 **Received From:** {received_from}  
🔹 **LOA Verification Status:** {loa_verification_status}  

"""
        
        if is_loa_correct:
            template += """✅ **The LOA has been verified as correct.**  

**Next Steps:**  
{next_action_required}  
**Additional Findings:** {additional_findings}  
"""
        else:
            template += """❌ **The LOA verification found issues that need to be addressed.**  

**Next Steps:**  
{next_action_required}  
**Additional Findings:** {additional_findings}  

Please provide an updated LOA with the correct information.
"""
        
        template += """
**Best Regards,**  
TE Connectivity Support Team
"""
        
        return format_response(data, template)
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return f" Database error occurred while processing your request: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")
# For S&D Claim Rejection Queries (Type 15)
def process_sd_claim_rejection_query(query):
    """Process Ship & Debit claim rejection queries."""
    print(f"🔍 Processing S&D claim rejection query: {query}")
    
    # Extract claim ID using extract_id function
    claim_id = extract_id(query, r'claim\s+(?:id|#)?\s*[:=]?\s*(\w+[-\d]*)', "Could not find a valid Claim ID in the query")
    
    # Extract quote ID if available
    quote_id = extract_id(query, r'quote\s+(?:id|#)?\s*[:=]?\s*#?(\d{10})', "Could not find a valid Quote ID in the query")
    
    # Check if we have at least one identifier
    if not claim_id and not quote_id:
        return " Could not find a valid Claim ID or Quote ID in your query. Please provide either a Claim ID or a 10-digit Quote ID."
    
    print(f"📝 Extracted Claim ID: {claim_id}, Quote ID: {quote_id}")
    
    try:
        conn = get_database_connection()
        if not conn:
            return " Database connection error. Please try again later."
        
        cursor = conn.cursor(dictionary=True)
        
        result = None
        
        # Try to find by claim_id first if available
        if claim_id:
            query = """SELECT * FROM 15_s_d_claim_rejection WHERE claim_id = %s"""
            cursor.execute(query, (claim_id,))
            result = cursor.fetchone()
        
        # If no result and we have quote_id, try that
        if not result and quote_id:
            query = """SELECT * FROM 15_s_d_claim_rejection WHERE quote_id = %s"""
            cursor.execute(query, (quote_id,))
            result = cursor.fetchone()
        
        if not result:
            id_used = f"Claim ID: {claim_id}" if claim_id else f"Quote ID: {quote_id}"
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for {id_used}**

We couldn't find details regarding this S&D claim rejection in our database.
Please verify the information and try again, or provide additional details.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        response = f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

🔹 **Claim ID:** {result.get('claim_id', 'N/A')}  
🔹 **Associated Quote ID:** {result.get('quote_id', 'N/A')}  
🔹 **Rejection Reason:** {result.get('rejection_reason', 'N/A')}  

**Next Steps:**  
{result.get('next_action_required', 'The claim rejection has been verified. Please address the rejection reason and resubmit if applicable.')}  

**Additional Information:**  
{result.get('additional_findings', 'N/A')}  

🔗 Please contact the S&D team for further assistance if needed.

**Best Regards,**  
TE Connectivity Support Team
"""
        return response
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return f" Database error occurred while processing your request: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")

# -------------------------- Agreement PN Addition/Removal Queries (Type 16) --------------------------
def process_agreement_pn_query(query):
    """Process agreement part number addition/removal queries."""
    print(f"🔍 Processing agreement PN query: {query}")
    
    # Extract agreement ID using extract_id function
    agreement_id = extract_id(query, r'agreement\s+(?:id|#)?\s*[:=]?\s*(\w+[-\d]*)', 
                            "Could not find a valid Agreement ID in the query")
    
    # Extract part number if available
    part_number = extract_id(query, r'(?:part|pn|p/n)\s+(?:number|#)?\s*[:=]?\s*(\w+[-\d]*)', "Could not find a valid Part Number in the query")
    
    print(f"📝 Extracted Agreement ID: {agreement_id}, Part Number: {part_number}")
    
    # Check if we have at least one identifier
    if not agreement_id and not part_number:
        return " Could not find a valid Agreement ID or Part Number in your query. Please provide at least one of these identifiers."
    
    # Determine request type
    request_type = "Unknown"
    if re.search(r'add|addition|include', query, re.IGNORECASE):
        request_type = "Addition"
    elif re.search(r'remov|delet|exclud', query, re.IGNORECASE):
        request_type = "Removal"
    
    try:
        conn = get_database_connection()
        if not conn:
            return " Database connection error. Please try again later."
        
        cursor = conn.cursor(dictionary=True)
        
        result = None
        
        # Try to find by agreement_id first if available
        if agreement_id:
            query = """SELECT * FROM 16_agreement_pn_addition WHERE agreement_id = %s"""
            cursor.execute(query, (agreement_id,))
            result = cursor.fetchone()
        
        # If no result and we have part_number, try that
        if not result and part_number:
            query = """SELECT * FROM 16_agreement_pn_addition WHERE part_number = %s"""
            cursor.execute(query, (part_number,))
            result = cursor.fetchone()
        
        if not result:
            id_used = []
            if agreement_id:
                id_used.append(f"Agreement ID: {agreement_id}")
            if part_number:
                id_used.append(f"Part Number: {part_number}")
            
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**No information found for {' and '.join(id_used)}**

We couldn't find details regarding this agreement part number request in our database.
Please verify the information and try again, or provide additional details.

**Best Regards,**  
TE Connectivity Support Team
"""
        
        response = f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

🔹 **Agreement ID:** {result.get('agreement_id', 'N/A')}  
🔹 **Part Number:** {result.get('part_number', 'N/A')}  
🔹 **Request Type:** {result.get('request_type', request_type)}  
🔹 **Requested By:** {result.get('requested_by', 'N/A')}  
🔹 **Approval Status:** {result.get('approval_status', 'N/A')}  

**Next Steps:**  
{result.get('next_action_required', 'This request has been forwarded to the agreement owner for review.')}  

**Additional Information:**  
{result.get('additional_findings', 'N/A')}  

**Best Regards,**  
TE Connectivity Support Team
"""
        return response
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return f" Database error occurred while processing your request: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")

# -------------------------- TE.com Issues Queries (Type 17) --------------------------
def process_te_com_issues_query(query):
    """Process TE.com website issues queries."""
    print(f"🔍 Processing TE.com issue query: {query}")
    
    # Extract issue ID using extract_id function
    issue_id = extract_id(query, r'issue\s+(?:id|#|ticket)?\s*[:=]?\s*(\w+[-\d]*)', "Could not find a valid Issue ID in the query")
    
    # Extract part number if available
    part_number = extract_id(query, r'(?:part|pn|p/n)\s+(?:number|#)?\s*[:=]?\s*(\w+[-\d]*)', 
                            "Could not find a valid Part Number in the query")
    
    print(f"📝 Extracted Issue ID: {issue_id}, Part Number: {part_number}")
    
    # Determine issue type
    issue_type = "General"
    if re.search(r'spr|special\s+price', query, re.IGNORECASE):
        issue_type = "SPR Creation"
    elif re.search(r'login|sign\s+in', query, re.IGNORECASE):
        issue_type = "Login Issue"
    elif re.search(r'order|purchas', query, re.IGNORECASE):
        issue_type = "Order Placement"
    elif re.search(r'search|find', query, re.IGNORECASE):
        issue_type = "Search Functionality"
    
    try:
        conn = get_database_connection()
        if not conn:
            return " Database connection error. Please try again later."
        
        cursor = conn.cursor(dictionary=True)
        
        result = None
        
        # Try to find by issue_id first if available
        if issue_id:
            query = """SELECT * FROM 17_te_com_issues_queries WHERE issue_id = %s"""
            cursor.execute(query, (issue_id,))
            result = cursor.fetchone()
        
        # If no result and we have part_number, try that
        if not result and part_number:
            query = """SELECT * FROM 17_te_com_issues_queries WHERE part_number = %s"""
            cursor.execute(query, (part_number,))
            result = cursor.fetchone()
        
        if not result:
            # Standard response for TE.com issues when no database record is found
            return f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

**Regarding your TE.com Website Issue**

We have received your query regarding an issue with TE.com. For website technical issues, 
we recommend creating a support ticket through the TE.com support portal:

1. Go to TE.com and log in to your account
2. Navigate to "Support" > "Contact Support"
3. Complete the support form with details of the issue you're experiencing

If you are unable to access the support form, please email support@te.com with:
- A detailed description of the issue
- Screenshots showing the problem (if applicable)
- Your account information
- Part numbers affected (if applicable)

**Best Regards,**  
TE Connectivity Support Team
"""
        
        response = f"""
📅 **Date:** {datetime.now().strftime("%B %d, %Y")}

🔹 **Issue ID:** {result.get('issue_id', 'N/A')}  
🔹 **Part Number Affected:** {result.get('part_number', 'N/A')}  
🔹 **Issue Type:** {result.get('issue_type', issue_type)}  

**Next Steps:**  
{result.get('next_action_required', 'Please create a support ticket through the TE.com portal for faster resolution of your issue.')}  

**Additional Information:**  
{result.get('additional_findings', 'N/A')}  

**Best Regards,**  
TE Connectivity Support Team
"""
        return response
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return f" Database error occurred while processing your request: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Database connection closed")