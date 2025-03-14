"use client"

import { useState } from "react"
import { Search, Send, Sparkles } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Textarea } from "@/components/ui/textarea"
import { ManualReplyList } from "@/components/manual-reply/manual-reply-list"
import { ManualReplyDetail } from "@/components/manual-reply/manual-reply-detail"

export default function ManualReplyPage() {
  const [selectedEmail, setSelectedEmail] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [replySubject, setReplySubject] = useState("")
  const [replyContent, setReplyContent] = useState("")
  const [isSearchingSimilar, setIsSearchingSimilar] = useState(false)

  const handleSearchSimilar = () => {
    setIsSearchingSimilar(true)

    // Simulate searching for similar emails
    setTimeout(() => {
      if (selectedEmail === "m1") {
        // POS Replace template
        setReplySubject("RE: POS Replace Request - Complex Case")
        setReplyContent(`Dear Distributor Rep,

Thank you for your inquiry regarding the POS update on quote 500987654 to XYZ Manufacturing.

Upon reviewing the case, I can confirm that there is indeed a conflict with the existing agreement ABC123 for XYZ Manufacturing. In this situation, we cannot simply replace the POS as requested due to the different pricing terms.

You have two options:

1. Create a new quote specifically for XYZ Manufacturing that aligns with their existing agreement ABC123.
2. Request an exception from the agreement owner to allow this specific quote to use different terms than the existing agreement.

If you would like to proceed with option 2, please provide a business justification for the exception, and we will forward it to the appropriate team for review.

Please let me know how you would like to proceed.

Best regards,
Support Team`)
      } else if (selectedEmail === "m3") {
        // S&D Claim Rejection template
        setReplySubject("RE: S&D Claim Rejection Query")
        setReplyContent(`Dear Partner Account,

Thank you for your inquiry regarding the rejected S&D claim #CL123456.

I've investigated this case with the S&D team and found that the claim was rejected for the following reason:

The invoice date falls outside the valid claim period for agreement P000789. According to our records, claims must be submitted within 60 days of the invoice date, but this claim was submitted 75 days after the invoice date.

If you believe this is incorrect, please provide the following documentation:
1. A copy of the original invoice showing the correct date
2. Proof of shipment date
3. Any communication that may have extended the claim period for this agreement

Once we receive this information, we can request a review of the rejection decision.

Please let me know if you have any questions.

Best regards,
Support Team`)
      } else if (selectedEmail === "m5") {
        // SFDC Rejection template
        setReplySubject("RE: SFDC Opportunity Rejected Incorrectly")
        setReplyContent(`Dear Sales Representative,

Thank you for bringing this to our attention regarding opportunity #500654321.

I've reviewed the rejection reason and the information you've provided. Unfortunately, once an opportunity has been rejected in SFDC, it cannot be reopened or reversed.

The opportunity #500654321 has been rejected on SFDC and unfortunately this cannot be revoked. Kindly ask the customer to raise another new opportunity with the correct customer chain and share with us the reference number immediately to avoid potential rejections again.

To ensure the new opportunity is processed correctly, please make sure to:
1. Verify all customer chain information is accurate
2. Include a reference to the previously rejected opportunity
3. Mark it as urgent to expedite processing

Once the new opportunity is submitted, please send me the new reference number, and I'll monitor it to ensure it's processed promptly.

Best regards,
Support Team`)
      } else {
        // Generic template
        setReplySubject(
          `RE: ${
            selectedEmail === "m2"
              ? "LOA Query - Missing Information"
              : selectedEmail === "m4"
                ? "Agreement PN Addition Request"
                : selectedEmail === "m6"
                  ? "TE.com SPR Issue for Multiple PNs"
                  : selectedEmail === "m7"
                    ? "Quote Routing Issue - Not Reaching GPMS"
                    : "Piggyback Creation with Special Terms"
          }`,
        )
        setReplyContent(`Dear ${
          selectedEmail === "m2"
            ? "Enterprise Manager"
            : selectedEmail === "m4"
              ? "Customer Support"
              : selectedEmail === "m6"
                ? "Distributor Support"
                : selectedEmail === "m7"
                  ? "Account Manager"
                  : "Partner Manager"
        },

Thank you for your inquiry. I've reviewed your request and am working on a solution.

I'll need to gather some additional information from our internal teams to properly address your specific case. I expect to have a complete response for you within the next 24 hours.

In the meantime, if you have any additional details that might help expedite this process, please feel free to share them.

Thank you for your patience.

Best regards,
Support Team`)
      }
      setIsSearchingSimilar(false)
    }, 1500)
  }

  const handleSendReply = () => {
    // Handle sending the reply
    alert("Reply sent successfully!")
    setSelectedEmail(null)
    setReplySubject("")
    setReplyContent("")
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="flex h-16 items-center px-4 gap-4">
          <SidebarTrigger />
          <h1 className="text-xl font-semibold">Manual Reply</h1>
          <div className="ml-auto flex items-center gap-2">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search emails..."
                className="pl-8 w-[250px]"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        <div className="w-full md:w-1/3 border-r">
          <div className="p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Pending Replies</h2>
              <div className="text-sm font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300 px-2 py-1 rounded-md">
                28 Pending
              </div>
            </div>
            <ManualReplyList searchQuery={searchQuery} selectedEmail={selectedEmail} onSelectEmail={setSelectedEmail} />
          </div>
        </div>

        <div className="hidden md:block md:flex-1">
          {selectedEmail ? (
            <div className="flex flex-col h-full">
              <ManualReplyDetail emailId={selectedEmail} />

              <div className="p-4 border-t">
                <Card>
                  <CardHeader>
                    <CardTitle>Compose Reply</CardTitle>
                    <CardDescription>Respond to this email with a personalized message</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Input
                        placeholder="Subject"
                        value={replySubject}
                        onChange={(e) => setReplySubject(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Textarea
                        placeholder="Write your reply here..."
                        className="min-h-[200px]"
                        value={replyContent}
                        onChange={(e) => setReplyContent(e.target.value)}
                      />
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between">
                    <Button variant="outline" onClick={handleSearchSimilar} disabled={isSearchingSimilar}>
                      <Sparkles className="mr-2 h-4 w-4" />
                      {isSearchingSimilar ? "Searching..." : "Find Similar Reply"}
                    </Button>
                    <Button onClick={handleSendReply} disabled={!replyContent.trim() || !replySubject.trim()}>
                      <Send className="mr-2 h-4 w-4" />
                      Send Reply
                    </Button>
                  </CardFooter>
                </Card>
              </div>
            </div>
          ) : (
            <div className="flex h-full items-center justify-center">
              <Card className="mx-auto max-w-md">
                <CardHeader>
                  <CardTitle>No Email Selected</CardTitle>
                  <CardDescription>Select an email from the list to compose a manual reply</CardDescription>
                </CardHeader>
                <CardContent className="flex justify-center">
                  <Send className="h-16 w-16 text-muted-foreground/50" />
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

