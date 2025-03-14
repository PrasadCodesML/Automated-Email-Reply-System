import { formatDistanceToNow } from "date-fns"
import { ArrowLeft, ArrowRight, MoreHorizontal, Reply, Trash2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

interface EmailDetailProps {
  emailId: string
}

// This would typically come from an API
const getEmailById = (id: string) => {
  return {
    id,
    from: {
      name:
        id === "e1"
          ? "Distributor Rep"
          : id === "e2"
            ? "Partner Manager"
            : id === "e3"
              ? "Distributor Rep"
              : id === "e4"
                ? "Customer Account"
                : id === "e5"
                  ? "Partner Manager"
                  : id === "e6"
                    ? "Sales Representative"
                    : id === "e7"
                      ? "Account Manager"
                      : "Customer Support",
      email:
        id === "e1"
          ? "distributor@example.com"
          : id === "e2"
            ? "partner@example.com"
            : id === "e3"
              ? "distributor@example.com"
              : id === "e4"
                ? "customer@example.com"
                : id === "e5"
                  ? "partner@example.com"
                  : id === "e6"
                    ? "sales@example.com"
                    : id === "e7"
                      ? "account-manager@example.com"
                      : "customer@example.com",
    },
    to: "support@company.com",
    subject:
      id === "e1"
        ? "POS Replace Request - Quote #500123456"
        : id === "e2"
          ? "General Pricing Query - Quote Extension"
          : id === "e3"
            ? "Piggyback Creation Request with LOA"
            : id === "e4"
              ? "Adding Parts to Existing Piggyback P000123"
              : id === "e5"
                ? "Ship & Debit Query - Conversion from FSA"
                : id === "e6"
                  ? "Opportunity #500123456 Rejected on SFDC"
                  : id === "e7"
                    ? "Pending Approval on SFDC #500789012"
                    : "Unable to Get Quote Document for #500345678",
    body:
      id === "e1"
        ? `<p>Hello Support Team,</p>
           <p>This is with regards to POS update on quote 500123456 to ABC Electronics (new POS customer name). Upon checking we found no potential conflicts with new POS customers.</p>
           <p>Could you please advise if it's ok to replace POS as requested?</p>
           <p>Quote details:</p>
           <ul>
             <li>Quote Number: 500123456</li>
             <li>Current POS: XYZ Corporation</li>
             <li>Requested New POS: ABC Electronics</li>
             <li>Part Numbers: PN123, PN456, PN789</li>
           </ul>
           <p>Thank you for your assistance.</p>
           <p>Best regards,<br>Distributor Rep</p>`
        : id === "e2"
          ? `<p>Dear Support,</p>
           <p>We need to extend the validity of quote #500789012 as the customer is still finalizing their requirements. The current validity ends on 15th July.</p>
           <p>Could you please extend the validity for another 30 days?</p>
           <p>Quote details:</p>
           <ul>
             <li>Quote Number: 500789012</li>
             <li>Current Validity: July 15, 2023</li>
             <li>Requested Extension: August 15, 2023</li>
             <li>Customer: DEF Industries</li>
           </ul>
           <p>Thank you for your help.</p>
           <p>Regards,<br>Partner Manager</p>`
          : id === "e3"
            ? `<p>Hello,</p>
           <p>We received a request from XYZ Distributor to create piggyback for the following part numbers (PNs) and/or POS customers which is linked to the OEM agreement ABC123.</p>
           <p>Please find the attached LOA and advise if any additional uplift need to be added.</p>
           <p>Details:</p>
           <ul>
             <li>Distributor: XYZ Distributor</li>
             <li>OEM Agreement: ABC123</li>
             <li>Part Numbers: PN001, PN002, PN003</li>
             <li>POS Customers: Customer A, Customer B</li>
           </ul>
           <p>The LOA is attached to this email for your reference.</p>
           <p>Looking forward to your response.</p>
           <p>Best regards,<br>Distributor Rep</p>`
            : id === "e4"
              ? `<p>Dear Support Team,</p>
           <p>We received a request from ABC Distributor to add the following part numbers (PNs) and/or POS customers to the existing Piggyback P000123, which is linked to the OEM agreement XYZ456.</p>
           <p>Details:</p>
           <ul>
             <li>Existing Piggyback: P000123</li>
             <li>OEM Agreement: XYZ456</li>
             <li>Additional Part Numbers: PN789, PN101, PN202</li>
             <li>Additional POS Customers: Customer X, Customer Y</li>
           </ul>
           <p>Please let us know if you need any additional information to process this request.</p>
           <p>Thank you,<br>Customer Account</p>`
              : id === "e5"
                ? `<p>Hello Support,</p>
           <p>We need to convert the following FSA to Ship & Debit for customer ABC Electronics. The current FSA number is FSA123456.</p>
           <p>Details:</p>
           <ul>
             <li>Current FSA: FSA123456</li>
             <li>Customer: ABC Electronics</li>
             <li>Part Numbers: PN111, PN222, PN333</li>
             <li>Reason for Conversion: Customer preference for backend rebate process</li>
           </ul>
           <p>Could you please advise on the process and timeline for this conversion?</p>
           <p>Best regards,<br>Partner Manager</p>`
                : id === "e6"
                  ? `<p>Dear Support,</p>
           <p>The opportunity #500123456 has been rejected on SFDC. Could you please check the reason for rejection and advise if we can resubmit with corrections?</p>
           <p>Details:</p>
           <ul>
             <li>Opportunity Number: 500123456</li>
             <li>Customer: GHI Corporation</li>
             <li>Products: Product A, Product B</li>
             <li>Submission Date: July 5, 2023</li>
           </ul>
           <p>The customer is waiting for this quote urgently, so any assistance to expedite would be appreciated.</p>
           <p>Thank you,<br>Sales Representative</p>`
                  : id === "e7"
                    ? `<p>Hello,</p>
           <p>Could you please approve the opportunity #500789012 pending with you for review on SFDC and push it to pricing. The customer is urgently waiting for the quote.</p>
           <p>Details:</p>
           <ul>
             <li>Opportunity Number: 500789012</li>
             <li>Customer: JKL Industries</li>
             <li>Products: Product X, Product Y, Product Z</li>
             <li>Value: $45,000</li>
             <li>Pending Since: July 8, 2023</li>
           </ul>
           <p>Please let me know if you need any additional information.</p>
           <p>Regards,<br>Account Manager</p>`
                    : `<p>Dear Support Team,</p>
           <p>We are unable to retrieve the quote document for #500345678 which shows as closed on GPMS. Could you please help us get the document as we need to place the order urgently?</p>
           <p>Details:</p>
           <ul>
             <li>Quote Number: 500345678</li>
             <li>Customer: MNO Corporation</li>
             <li>Closed Date: July 1, 2023</li>
             <li>Required By: July 15, 2023</li>
           </ul>
           <p>Thank you for your assistance.</p>
           <p>Best regards,<br>Customer Support</p>`,
    time: new Date(
      Date.now() -
        1000 *
          60 *
          (id === "e1"
            ? 30
            : id === "e2"
              ? 60 * 2
              : id === "e3"
                ? 60 * 5
                : id === "e4"
                  ? 60 * 8
                  : id === "e5"
                    ? 60 * 24
                    : id === "e6"
                      ? 60 * 24 * 2
                      : id === "e7"
                        ? 60 * 24 * 3
                        : 60 * 24 * 4),
    ),
    status:
      id === "e1" || id === "e3"
        ? "new"
        : id === "e4" || id === "e5" || id === "e7" || id === "e8"
          ? "replied"
          : "manual",
    read: id === "e2" || id === "e4" || id === "e5" || id === "e7" || id === "e8",
  }
}

export function EmailDetail({ emailId }: EmailDetailProps) {
  const email = getEmailById(emailId)

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" className="md:hidden">
            <ArrowLeft className="h-4 w-4" />
            <span className="sr-only">Back</span>
          </Button>
          <h2 className="text-lg font-semibold">{email.subject}</h2>
          {email.status === "new" && (
            <Badge variant="outline" className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">
              New
            </Badge>
          )}
          {email.status === "replied" && (
            <Badge variant="outline" className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
              Auto-Replied
            </Badge>
          )}
          {email.status === "manual" && (
            <Badge variant="outline" className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
              Manual Reply
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon">
            <Reply className="h-4 w-4" />
            <span className="sr-only">Reply</span>
          </Button>
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

      <div className="p-4 border-t">
        <div className="flex gap-2">
          <Button className="w-full">
            <Reply className="mr-2 h-4 w-4" />
            Reply
          </Button>
          <Button variant="outline">
            <ArrowRight className="mr-2 h-4 w-4" />
            Forward
          </Button>
        </div>
      </div>
    </div>
  )
}

