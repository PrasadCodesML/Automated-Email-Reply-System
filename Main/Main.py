from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph, START
import os
import re
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
# Import all helper functions
from helper_functions import (
    process_pos_replacement_query,
    process_general_pricing_query,
    process_piggyback_creation_query,
    process_adding_parts_to_piggyback_query,
    process_ship_debit_query,
    process_opportunities_rejected_sfdc_query,
    process_pending_approval_sfdc_query,
    process_quote_closed_gpms_no_document_query,
    process_quote_not_reaching_pricing_query,
    process_customer_data_enquiries_query,
    process_gpms_pending_quotes,
    process_sfdc_pending_opportunities,
    process_opportunity_rejected_incorrectly,
    process_loa_related_queries,
    process_sd_claim_rejection_query,
    process_agreement_pn_query,
    process_te_com_issues_query
)

# Get API key from environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

# Initialize the LLM
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

class RouteQuery(BaseModel):
    """Route a user query to the correct processing logic."""
    category: Literal[
        "pos_replace",
        "general_pricing_queries",
        "piggyback_creation",
        "adding_parts_to_piggyback",
        "ship_and_debit_queries",
        "opportunities_rejected_sfdc",
        "pending_approval_sfdc",
        "quote_closed_gpms_no_document",
        "quote_not_reaching_pricing",
        "customer_data_enquiries",
        "quotes_pending_review_gpms",
        "opportunities_pending_review_sfdc",
        "opportunity_rejected_incorrectly_sfdc",
        "loa_related_queries",
        "s_and_d_claim_rejection",
        "agreement_pn_addition_removal",
        "te_com_issues",
        "product_enquiry",
        "feedback",
        "complaint",
        "fallback"
    ] = Field(..., description="Classify the user query into one of 21 specific routes.")

# Define routing prompt template
router_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a routing assistant for TE Connectivity's support team.
Your task is to analyze customer queries and classify them into the correct category.
Available categories:
1. pos_replace - Issues regarding POS replacement on quotes.
2. general_pricing_queries - Queries about price adjustments, volume discounts, validity, extensions, etc.
3. piggyback_creation - Requests to create a piggyback linked to an OEM agreement.
4. adding_parts_to_piggyback - Requests to add parts or POS customers to an existing piggyback.
5. ship_and_debit_queries - Queries about Ship & Debit, FSA to S&D conversion, or POS/END customer addresses.
6. opportunities_rejected_sfdc - Queries about opportunities rejected in Salesforce.
7. pending_approval_sfdc - Requests for approval of opportunities pending in Salesforce.
8. quote_closed_gpms_no_document - Cases where quote is closed in GPMS but customer can't get the document.
9. quote_not_reaching_pricing - Cases where a quote was raised but hasn't reached pricing.
10. customer_data_enquiries - Requests for customer data.
11. quotes_pending_review_gpms - Enquiries about quotes pending review in GPMS.
12. opportunities_pending_review_sfdc - Enquiries about opportunities pending review in Salesforce.
13. opportunity_rejected_incorrectly_sfdc - Cases where opportunities were incorrectly rejected in SFDC.
14. loa_related_queries - Letters of Authorization (LOA) related queries.
15. s_and_d_claim_rejection - Enquiries about Ship & Debit claim rejections.
16. agreement_pn_addition_removal - Agreement-related part number addition or removal.
17. te_com_issues - Issues with TE.com where customers can't raise SPRs or have issues with specific PNs.
18. product_enquiry - General questions about TE products.
19. feedback - Customer providing feedback.
20. complaint - Customer making a complaint.
21. fallback - Queries that don't fit any of the above categories.

Analyze the query carefully and choose only one category.
"""),
    ("human", "{question}")
])

# Create a callable chain to route queries
def route_with_llm(state):
    """Use LLM to determine the category of the query."""
    query = state["question"]
    chain = router_prompt | llm
    response = chain.invoke({"question": query})
    
    # Extract the category from the response
    response_text = response.content.lower()
    
    # Define category mappings
    category_mappings = {
        "pos_replace": ["pos replace", "pos replacement", "pos update"],
        "general_pricing_queries": ["pricing", "price adjust", "volume discount", "validity", "quote extension"],
        "piggyback_creation": ["piggyback creation", "create piggyback", "new piggyback"],
        "adding_parts_to_piggyback": ["add part", "add to piggyback", "existing piggyback"],
        "ship_and_debit_queries": ["ship", "debit", "s&d", "fsa to s&d", "fsa conversion"],
        "opportunities_rejected_sfdc": ["rejected opportunity", "sfdc rejection"],
        "pending_approval_sfdc": ["pending approval", "approve opportunity"],
        "quote_closed_gpms_no_document": ["closed quote", "no document", "quote document"],
        "quote_not_reaching_pricing": ["quote not reaching", "not reached pricing"],
        "customer_data_enquiries": ["customer data", "data enquiry", "data request"],
        "quotes_pending_review_gpms": ["quote pending", "gpms review"],
        "opportunities_pending_review_sfdc": ["opportunity pending", "sfdc review"],
        "opportunity_rejected_incorrectly_sfdc": ["incorrectly rejected", "wrong rejection"],
        "loa_related_queries": ["loa", "letter of authorization"],
        "s_and_d_claim_rejection": ["claim rejection", "s&d claim", "rejected claim"],
        "agreement_pn_addition_removal": ["agreement", "pn addition", "pn removal"],
        "te_com_issues": ["te.com", "website issue", "spr"],
        "product_enquiry": ["product", "product specs", "product details"],
        "feedback": ["feedback", "suggestion"],
        "complaint": ["complaint", "dissatisfied"]
    }
    
    # Check if any category keywords are in the response
    detected_category = "fallback"
    for category, keywords in category_mappings.items():
        if any(keyword in response_text for keyword in keywords):
            detected_category = category
            break
    
    # For rule-based overrides
    lower_query = query.lower()
    
    # S&D query detection
    if any(keyword in lower_query for keyword in ["ship", "debit", "s&d", "fsa", "sandd"]) or re.search(r'\b\d{10}\b', lower_query):
        if any(keyword in lower_query for keyword in ["claim", "reject"]):
            detected_category = "s_and_d_claim_rejection"
        else:
            detected_category = "ship_and_debit_queries"
    
    # TE.com issues detection
    if "te.com" in lower_query or "website" in lower_query or "spr" in lower_query:
        detected_category = "te_com_issues"
    
    # Agreement detection
    if "agreement" in lower_query and ("part" in lower_query or "pn" in lower_query):
        detected_category = "agreement_pn_addition_removal"
    
    print(f"🧭 Routing result: {detected_category}")
    return detected_category

# Handler functions for each category
def handle_pos_replace(state):
    """Handle POS replacement queries"""
    query = state["question"]
    response = process_pos_replacement_query(query)
    return {"response": response}

def handle_general_pricing(state):
    """Handle general pricing queries"""
    query = state["question"]
    response = process_general_pricing_query(query)
    return {"response": response}

def handle_piggyback_creation(state):
    """Handle piggyback creation queries"""
    query = state["question"]
    response = process_piggyback_creation_query(query)
    return {"response": response}

def handle_adding_parts_to_piggyback(state):
    """Handle adding parts to piggyback queries"""
    query = state["question"]
    response = process_adding_parts_to_piggyback_query(query)
    return {"response": response}

def handle_ship_and_debit_queries(state):
    """Handle ship and debit queries"""
    query = state["question"]
    response = process_ship_debit_query(query)
    return {"response": response}

def handle_opportunities_rejected_sfdc(state):
    """Handle opportunities rejected in SFDC queries"""
    query = state["question"]
    response = process_opportunities_rejected_sfdc_query(query)
    return {"response": response}

def handle_pending_approval_sfdc(state):
    """Handle pending approval in SFDC queries"""
    query = state["question"]
    response = process_pending_approval_sfdc_query(query)
    return {"response": response}

def handle_quote_closed_gpms_no_document(state):
    """Handle quote closed in GPMS with no document queries"""
    query = state["question"]
    response = process_quote_closed_gpms_no_document_query(query)
    return {"response": response}

def handle_quote_not_reaching_pricing(state):
    """Handle quote not reaching pricing queries"""
    query = state["question"]
    response = process_quote_not_reaching_pricing_query(query)
    return {"response": response}

def handle_customer_data_enquiries(state):
    """Handle customer data enquiries"""
    query = state["question"]
    response = process_customer_data_enquiries_query(query)
    return {"response": response}

def handle_quotes_pending_review_gpms(state):
    """Handle quotes pending review in GPMS queries"""
    query = state["question"]
    response = process_gpms_pending_quotes(query)
    return {"response": response}

def handle_opportunities_pending_review_sfdc(state):
    """Handle opportunities pending review in SFDC queries"""
    query = state["question"]
    response = process_sfdc_pending_opportunities(query)
    return {"response": response}

def handle_opportunity_rejected_incorrectly_sfdc(state):
    """Handle opportunity rejected incorrectly in SFDC queries"""
    query = state["question"]
    response = process_opportunity_rejected_incorrectly(query)
    return {"response": response}

def handle_loa_related_queries(state):
    """Handle LOA related queries"""
    query = state["question"]
    response = process_loa_related_queries(query)
    return {"response": response}

def handle_s_and_d_claim_rejection(state):
    """Handle S&D claim rejection queries"""
    query = state["question"]
    response = process_sd_claim_rejection_query(query)
    return {"response": response}

def handle_agreement_pn_addition_removal(state):
    """Handle agreement PN addition/removal queries"""
    query = state["question"]
    response = process_agreement_pn_query(query)
    return {"response": response}

def handle_te_com_issues(state):
    """Handle TE.com issues queries"""
    query = state["question"]
    response = process_te_com_issues_query(query)
    return {"response": response}

def handle_product_enquiry(state):
    """Handle product enquiry queries"""
    return {"response": """
Thank you for your product inquiry.

To better assist you, I'll need some additional information:
- Specific part number(s) you're interested in
- Application requirements
- Quantity needed
- Any specific technical specifications

Once I have these details, I can provide you with the appropriate product information or connect you with a product specialist.

Thank you,
TE Connectivity Support Team
"""}

def handle_feedback(state):
    """Handle feedback submissions"""
    return {"response": """
Thank you for sharing your feedback with TE Connectivity!

Your input is valuable to us and helps improve our products and services. I've recorded your feedback and will forward it to the appropriate team for review.

Is there anything else you'd like to share or any other way we can assist you today?

Thank you,
TE Connectivity Support Team
"""}

def handle_complaint(state):
    """Handle complaint submissions"""
    return {"response": """
I'm sorry to hear about your experience with TE Connectivity.

Your complaint has been logged and will be escalated to the appropriate department for immediate review. A customer service representative will contact you within 24-48 business hours to address your concerns.

Reference number: COM-{timestamp}

Thank you for bringing this to our attention.

TE Connectivity Support Team
""".format(timestamp=datetime.now().strftime("%Y%m%d%H%M"))}

def handle_fallback(state):
    """Handle fallback queries"""
    return {"response": """
⚠️ I'm sorry, but I couldn't classify your request into one of our standard categories.

Could you please provide more specific details about your query? For example:
- If it's about a quote, please provide the quote ID
- If it's about an opportunity, please provide the opportunity ID
- If it's about a specific agreement or part number, please include those details

This will help me route your query to the appropriate team for resolution.

Thank you,
TE Connectivity Support Team
"""}

# Create state graph
workflow = StateGraph(dict)

# Add all nodes to the graph
workflow.add_node("pos_replace", handle_pos_replace)
workflow.add_node("general_pricing_queries", handle_general_pricing)
workflow.add_node("piggyback_creation", handle_piggyback_creation)
workflow.add_node("adding_parts_to_piggyback", handle_adding_parts_to_piggyback)
workflow.add_node("ship_and_debit_queries", handle_ship_and_debit_queries)
workflow.add_node("opportunities_rejected_sfdc", handle_opportunities_rejected_sfdc)
workflow.add_node("pending_approval_sfdc", handle_pending_approval_sfdc)
workflow.add_node("quote_closed_gpms_no_document", handle_quote_closed_gpms_no_document)
workflow.add_node("quote_not_reaching_pricing", handle_quote_not_reaching_pricing)
workflow.add_node("customer_data_enquiries", handle_customer_data_enquiries)
workflow.add_node("quotes_pending_review_gpms", handle_quotes_pending_review_gpms)
workflow.add_node("opportunities_pending_review_sfdc", handle_opportunities_pending_review_sfdc)
workflow.add_node("opportunity_rejected_incorrectly_sfdc", handle_opportunity_rejected_incorrectly_sfdc)
workflow.add_node("loa_related_queries", handle_loa_related_queries)
workflow.add_node("s_and_d_claim_rejection", handle_s_and_d_claim_rejection)
workflow.add_node("agreement_pn_addition_removal", handle_agreement_pn_addition_removal)
workflow.add_node("te_com_issues", handle_te_com_issues)
workflow.add_node("product_enquiry", handle_product_enquiry)
workflow.add_node("feedback", handle_feedback)
workflow.add_node("complaint", handle_complaint)
workflow.add_node("fallback", handle_fallback)

# Define rule-based routing function
def route_question(state):
    """Rule-based routing with LLM backup."""
    question = state["question"]
    print(f"🧭 Processing question: {question}")
    
    # Use rule-based routing for clear cases
    if "pos" in question and ("replace" in question or "update" in question):
        print("Rule-based routing to: pos_replace")
        return "pos_replace"
    
    elif "price" in question or "pricing" in question or "discount" in question or "validity" in question:
        print("Rule-based routing to: general_pricing_queries")
        return "general_pricing_queries"
    
    elif "piggyback" in question and ("create" in question or "creation" in question or "new" in question):
        print("Rule-based routing to: piggyback_creation")
        return "piggyback_creation"
    
    elif "add" in question and "piggyback" in question:
        print("Rule-based routing to: adding_parts_to_piggyback")
        return "adding_parts_to_piggyback"
    
    elif any(keyword in question for keyword in ["ship", "debit", "s&d", "fsa", "sandd"]) and not "claim" in question:
        print("Rule-based routing to: ship_and_debit_queries")
        return "ship_and_debit_queries"
    
    elif "reject" in question and "sfdc" in question and not "incorrect" in question:
        print("Rule-based routing to: opportunities_rejected_sfdc")
        return "opportunities_rejected_sfdc"
    
    elif "pending approval" in question and "sfdc" in question:
        print("Rule-based routing to: pending_approval_sfdc")
        return "pending_approval_sfdc"
    
    elif "closed" in question and "gpms" in question and "document" in question:
        print("Rule-based routing to: quote_closed_gpms_no_document")
        return "quote_closed_gpms_no_document"
    
    elif "not reach" in question and "pricing" in question:
        print("Rule-based routing to: quote_not_reaching_pricing")
        return "quote_not_reaching_pricing"
    
    elif "customer data" in question or "data enquiry" in question or "data request" in question:
        print("Rule-based routing to: customer_data_enquiries")
        return "customer_data_enquiries"
    
    elif "pending" in question and "gpms" in question:
        print("Rule-based routing to: quotes_pending_review_gpms")
        return "quotes_pending_review_gpms"
    
    elif "pending" in question and "sfdc" in question and "opportunity" in question:
        print("Rule-based routing to: opportunities_pending_review_sfdc")
        return "opportunities_pending_review_sfdc"
    
    elif "incorrect" in question and "reject" in question:
        print("Rule-based routing to: opportunity_rejected_incorrectly_sfdc")
        return "opportunity_rejected_incorrectly_sfdc"
    
    elif "loa" in question or "letter of authorization" in question:
        print("Rule-based routing to: loa_related_queries")
        return "loa_related_queries"
    
    elif "claim" in question and any(term in question for term in ["s&d", "ship", "debit", "reject"]):
        print("Rule-based routing to: s_and_d_claim_rejection")
        return "s_and_d_claim_rejection"
    
    elif "agreement" in question and ("part" in question or "pn" in question):
        print("Rule-based routing to: agreement_pn_addition_removal")
        return "agreement_pn_addition_removal"
    
    elif "te.com" in question or "website" in question or "spr" in question:
        print("Rule-based routing to: te_com_issues")
        return "te_com_issues"
    
    elif "product" in question and any(term in question for term in ["spec", "detail", "information", "available"]):
        print("Rule-based routing to: product_enquiry")
        return "product_enquiry"
    
    elif "feedback" in question or "suggestion" in question:
        print("Rule-based routing to: feedback")
        return "feedback"
    
    elif "complaint" in question or "dissatisfied" in question:
        print("Rule-based routing to: complaint")
        return "complaint"
    
    # For more ambiguous cases, use LLM-based routing
    else:
        category = route_with_llm(state)
        print(f"LLM-based routing to: {category}")
        return category

# Add conditional edges from START to all possible nodes
workflow.add_conditional_edges(
    START,
    route_question,
    {
        "pos_replace": "pos_replace",
        "general_pricing_queries": "general_pricing_queries",
        "piggyback_creation": "piggyback_creation",
        "adding_parts_to_piggyback": "adding_parts_to_piggyback",
        "ship_and_debit_queries": "ship_and_debit_queries",
        "opportunities_rejected_sfdc": "opportunities_rejected_sfdc",
        "pending_approval_sfdc": "pending_approval_sfdc",
        "quote_closed_gpms_no_document": "quote_closed_gpms_no_document",
        "quote_not_reaching_pricing": "quote_not_reaching_pricing",
        "customer_data_enquiries": "customer_data_enquiries",
        "quotes_pending_review_gpms": "quotes_pending_review_gpms",
        "opportunities_pending_review_sfdc": "opportunities_pending_review_sfdc",
        "opportunity_rejected_incorrectly_sfdc": "opportunity_rejected_incorrectly_sfdc",
        "loa_related_queries": "loa_related_queries",
        "s_and_d_claim_rejection": "s_and_d_claim_rejection",
        "agreement_pn_addition_removal": "agreement_pn_addition_removal",
        "te_com_issues": "te_com_issues",
        "product_enquiry": "product_enquiry",
        "feedback": "feedback",
        "complaint": "complaint",
        "fallback": "fallback"
    }
)

# Add edges from all nodes to END
for node in [
    "pos_replace", "general_pricing_queries", "piggyback_creation", 
    "adding_parts_to_piggyback", "ship_and_debit_queries", 
    "opportunities_rejected_sfdc", "pending_approval_sfdc",
    "quote_closed_gpms_no_document", "quote_not_reaching_pricing",
    "customer_data_enquiries", "quotes_pending_review_gpms",
    "opportunities_pending_review_sfdc", "opportunity_rejected_incorrectly_sfdc",
    "loa_related_queries", "s_and_d_claim_rejection",
    "agreement_pn_addition_removal", "te_com_issues",
    "product_enquiry", "feedback", "complaint", "fallback"
]:
    workflow.add_edge(node, END)

# Compile the graph
app = workflow.compile()

# Function to process a query
def process_query(query):
    """Process a single query through the workflow."""
    print(f"📝 Processing query: {query}")
    result = app.invoke({"question": query})
    return result["response"]

# Example usage
if __name__ == "__main__":
    # Test queries
    test_queries = [
        "I need to update the POS on my quote QTID1",
        "Can I get a price discount on my order, my quote id is QTID45?",
        "My quote hasn't reached pricing yet QTID4",
        "How do I create a new piggyback for ABC Manufacturing my request_id PBK93584, Distributor D Ltd?",
        "I need to add parts to an existing piggyback for piggyback id ADD62889",
        "How do I setup a ship and debit agreement my QTID5008486211?",
        # "My opportunity was rejected in SFDC",
        # "When will my opportunity be approved in SFDC?",
        # "I can't find my quote document in GPMS",
        "Can you provide customer data for ABC Corp for quote id CDE36179?",
        "My opportunity is pending review in SFDC ",
        "My opportunity was rejected incorrectly",
        "I need help with an LOA",
        "My S&D claim was rejected",
        "I need to add parts to my agreement",
        "I can't access TE.com",
        "What are the specifications for product XYZ?",
        "I'd like to provide feedback on your service",
        "I want to make a complaint about my order"
    ]
    
    # Run test queries
    for query in test_queries:
        print("\n" + "="*50)
        response = process_query(query)
        print(f"🤖 Response: {response}")
        print("="*50 + "\n")