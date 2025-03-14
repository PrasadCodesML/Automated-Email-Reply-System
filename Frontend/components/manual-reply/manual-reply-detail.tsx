import { formatDistanceToNow } from "date-fns"
import { ArrowLeft, MoreHorizontal, Trash2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

interface ManualReplyDetailProps {
  emailId: string
}

// This would typically come from an API
const getEmailById = (id: string) => {
  return {
    id,
    from: {
      name:
        id === "m1"
          ? "Distributor Rep"
          : id === "m2"
            ? "Enterprise Manager"
            : id === "m3"
              ? "Partner Account"
              : id === "m4"
                ? "Customer Support"
                : id === "m5"
                  ? "Sales Representative"
                  : id === "m6"
                    ? "Distributor Support"
                    : id === "m7"
                      ? "Account Manager"
                      : "Partner Manager",
      email:
        id === "m1"
          ? "distributor@example.com"
          : id === "m2"
            ? "enterprise@example.com"
            : id === "m3"
              ? "partner@example.com"
              : id === "m4"
                ? "customer@example.com"
                : id === "m5"
                  ? "sales@example.com"
                  : id === "m6"
                    ? "distributor@example.com"
                    : id === "m7"
                      ? "account@example.com"
                      : "partner@example.com",
    },
    to: "support@company.com",
    subject:
      id === "m1"
        ? "POS Replace Request - Complex Case"
        : id === "m2"
          ? "LOA Query - Missing Information"
          : id === "m3"
            ? "S&D Claim Rejection Query"
            : id === "m4"
              ? "Agreement PN Addition Request"
              : id === "m5"
                ? "SFDC Opportunity Rejected Incorrectly"
                : id === "m6"
                  ? "TE.com SPR Issue for Multiple PNs"
                  : id === "m7"
                    ? "Quote Routing Issue - Not Reaching GPMS"
                    : "Piggyback Creation with Special Terms",
    body:
      id === "m1"
        ? `<p>Hello Support Team,</p>
           <p>This is with regards to POS update on quote 500987654 to XYZ Manufacturing (new POS customer name). Upon checking we found potential conflicts with new POS customers.</p>
           <p>Specifically, the new POS customer already has a different pricing agreement in place (Agreement #ABC123) with different terms than what's in the current quote.</p>
           <p>Quote details:</p>
           <ul>
             <li>Quote Number: 500987654</li>
             <li>Current POS: DEF Corporation</li>
             <li>Requested New POS: XYZ Manufacturing</li>
             <li>Part Numbers: PN123, PN456, PN789</li>
             <li>Conflicting Agreement: ABC123</li>
           </ul>
           <p>Could you please advise if it's still possible to replace the POS as requested, or if we need to create a new quote with different terms?</p>
           <p>Thank you for your assistance.</p>
           <p>Best regards,<br>Distributor Rep</p>`
        : id === "m2"
          ? `<p>Dear Support,</p>
           <p>We received an LOA for agreement ABC789 but there are several missing details. The LOA doesn't specify the authorized part numbers and the validity period is unclear.</p>
           <p>Issues with the LOA:</p>
           <ul>
             <li>Missing authorized part numbers</li>
             <li>Unclear validity period</li>
             <li>No specified pricing terms</li>
             <li>Missing authorized distributor information</li>
           </ul>
           <p>Could you please advise what specific information we need to request from the customer to complete this LOA properly?</p>
           <p>The agreement is critical for an upcoming project and we need to resolve this urgently.</p>
           <p>Thank you,<br>Enterprise Manager</p>`
          : id === "m3"
            ? `<p>Hello,</p>
           <p>Our S&D claim #CL123456 was rejected and we need to understand the reason. The claim was for customer DEF Industries under agreement P000789.</p>
           <p>Claim details:</p>
           <ul>
             <li>Claim Number: CL123456</li>
             <li>Agreement: P000789</li>
             <li>Customer: DEF Industries</li>
             <li>Part Numbers: PN111, PN222, PN333</li>
             <li>Claim Amount: $12,500</li>
             <li>Submission Date: July 5, 2023</li>
           </ul>
           <p>We've verified that all the information in the claim is accurate and matches our records. Could you please check with the S&D team to understand the specific reason for rejection?</p>
           <p>Best regards,<br>Partner Account</p>`
            : id === "m4"
              ? `<p>Dear Support Team,</p>
           <p>We need to add the following part numbers to our existing agreement ABC456: PN555, PN666, PN777. These parts are critical for our upcoming project.</p>
           <p>Agreement details:</p>
           <ul>
             <li>Agreement Number: ABC456</li>
             <li>Customer: GHI Corporation</li>
             <li>Current Parts: PN111, PN222, PN333</li>
             <li>Additional Parts Needed: PN555, PN666, PN777</li>
             <li>Project Start Date: August 1, 2023</li>
           </ul>
           <p>Could you please advise on the process and timeline for adding these parts to the agreement? We need to have this completed by July 25 to meet our project timeline.</p>
           <p>Thank you,<br>Customer Support</p>`
              : id === "m5"
                ? `<p>Hello Support,</p>
           <p>The opportunity #500654321 has been rejected on SFDC but we believe this was done incorrectly. The customer chain information was accurate.</p>
           <p>Opportunity details:</p>
           <ul>
             <li>Opportunity Number: 500654321</li>
             <li>Customer: JKL Industries</li>
             <li>End Customer: MNO Corporation</li>
             <li>Products: Product A, Product B</li>
             <li>Submission Date: July 10, 2023</li>
             <li>Rejection Date: July 11, 2023</li>
             <li>Rejection Reason: "Incorrect customer chain"</li>
           </ul>
           <p>We've verified with the customer that the chain information is correct. Is there a way to reopen this opportunity or do we need to create a new one?</p>
           <p>The customer is waiting for this quote urgently.</p>
           <p>Regards,<br>Sales Representative</p>`
                : id === "m6"
                  ? `<p>Dear Support,</p>
           <p>Our customer is unable to raise SPRs on TE.com for the following part numbers: PN888, PN999, PN101. They've tried multiple times but keep getting error messages.</p>
           <p>Details:</p>
           <ul>
             <li>Customer: PQR Electronics</li>
             <li>TE.com Account: user@pqr.com</li>
             <li>Part Numbers: PN888, PN999, PN101</li>
             <li>Error Message: "Unable to process request. Please contact support."</li>
           </ul>
           <p>The customer has tried using different browsers and clearing cache but the issue persists. Could you please help resolve this issue?</p>
           <p>Thank you,<br>Distributor Support</p>`
                  : id === "m7"
                    ? `<p>Hello,</p>
           <p>We raised quote #500333444 but it hasn't reached GPMS for pricing. The customer has been waiting for over a week and we need to expedite this.</p>
           <p>Quote details:</p>
           <ul>
             <li>Quote Number: 500333444</li>
             <li>Customer: STU Industries</li>
             <li>Products: Product X, Product Y</li>
             <li>Submission Date: July 5, 2023</li>
             <li>Current Status: "Submitted" (not showing in GPMS)</li>
           </ul>
           <p>Could you please check if there are any blocks preventing the quote from entering GPMS and help resolve this issue?</p>
           <p>Best regards,<br>Account Manager</p>`
                    : `<p>Dear Support Team,</p>
           <p>We need to create a piggyback for distributor GHI with special pricing terms. This is linked to OEM agreement DEF789 and requires management approval.</p>
           <p>Details:</p>
           <ul>
             <li>Distributor: GHI Distribution</li>
             <li>OEM Agreement: DEF789</li>
             <li>Part Numbers: PN123, PN456, PN789</li>
             <li>Special Terms: 5% additional discount on volume orders</li>
             <li>POS Customers: Customer X, Customer Y</li>
           </ul>
           <p>We have the LOA from the OEM authorizing this piggyback. Could you please advise on the next steps and if any additional approvals are needed?</p>
           <p>Thank you,<br>Partner Manager</p>`,
    time: new Date(
      Date.now() -
        1000 *
          60 *
          (id === "m1"
            ? 15
            : id === "m2"
              ? 45
              : id === "m3"
                ? 90
                : id === "m4"
                  ? 180
                  : id === "m5"
                    ? 240
                    : id === "m6"
                      ? 300
                      : id === "m7"
                        ? 360
                        : 420),
    ),
    priority:
      id === "m1" || id === "m2" || id === "m5" || id === "m8"
        ? "high"
        : id === "m3" || id === "m4" || id === "m7"
          ? "medium"
          : "low",
  }
}

export function ManualReplyDetail({ emailId }: ManualReplyDetailProps) {
  const email = getEmailById(emailId)

  return (
    <div className="flex flex-col h-full overflow-auto">
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" className="md:hidden">
            <ArrowLeft className="h-4 w-4" />
            <span className="sr-only">Back</span>
          </Button>
          <h2 className="text-lg font-semibold">{email.subject}</h2>
          {email.priority === "high" && (
            <Badge variant="outline" className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">
              High Priority
            </Badge>
          )}
          {email.priority === "medium" && (
            <Badge variant="outline" className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">
              Medium Priority
            </Badge>
          )}
          {email.priority === "low" && (
            <Badge variant="outline" className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
              Low Priority
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon">
            <Trash2 className="h-4 w-4" />
            <span className="sr-only">Delete</span>
          </Button>
          <Button variant="ghost" size="icon">
            <MoreHorizontal className="h-4 w-4" />
            <span className="sr-only">More</span>
          </Button>
        </div>
      </div>

      <div className="p-4 space-y-4 flex-1 overflow-auto">
        <div className="flex items-start gap-4">
          <Avatar>
            <AvatarFallback>
              {email.from.name
                .split(" ")
                .map((n) => n[0])
                .join("")}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold">{email.from.name}</div>
                <div className="text-sm text-muted-foreground">{email.from.email}</div>
              </div>
              <div className="text-sm text-muted-foreground">
                {formatDistanceToNow(email.time, { addSuffix: true })}
              </div>
            </div>
            <div className="text-sm text-muted-foreground mt-1">To: {email.to}</div>
          </div>
        </div>

        <Separator />

        <div className="prose prose-sm dark:prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: email.body }} />
      </div>
    </div>
  )
}

