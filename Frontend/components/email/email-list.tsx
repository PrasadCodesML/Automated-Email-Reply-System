"use client"

import { formatDistanceToNow } from "date-fns"

import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"

interface EmailListProps {
  filter: "all" | "new" | "replied" | "manual"
  searchQuery: string
  selectedEmail: string | null
  onSelectEmail: (id: string) => void
}

const emails = [
  {
    id: "e1",
    from: "distributor@example.com",
    subject: "POS Replace Request - Quote #500123456",
    preview:
      "This is with regards to POS update on quote 500123456 to ABC Electronics (new POS customer name). Upon checking we found no potential conflicts with new POS customers...",
    time: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
    status: "new",
    read: false,
  },
  {
    id: "e2",
    from: "partner@example.com",
    subject: "General Pricing Query - Quote Extension",
    preview:
      "We need to extend the validity of quote #500789012 as the customer is still finalizing their requirements. The current validity ends on 15th July...",
    time: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
    status: "manual",
    read: true,
  },
  {
    id: "e3",
    from: "distributor@example.com",
    subject: "Piggyback Creation Request with LOA",
    preview:
      "We received a request from XYZ Distributor to create piggyback for the following part numbers (PNs) and/or POS customers which is linked to the OEM agreement ABC123...",
    time: new Date(Date.now() - 1000 * 60 * 60 * 5), // 5 hours ago
    status: "new",
    read: false,
  },
  {
    id: "e4",
    from: "customer@example.com",
    subject: "Adding Parts to Existing Piggyback P000123",
    preview:
      "We received a request from ABC Distributor to add the following part numbers (PNs) and/or POS customers to the existing Piggyback P000123, which is linked to the OEM agreement XYZ456...",
    time: new Date(Date.now() - 1000 * 60 * 60 * 8), // 8 hours ago
    status: "replied",
    read: true,
  },
  {
    id: "e5",
    from: "partner@example.com",
    subject: "Ship & Debit Query - Conversion from FSA",
    preview:
      "We need to convert the following FSA to Ship & Debit for customer ABC Electronics. The current FSA number is FSA123456...",
    time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
    status: "replied",
    read: true,
  },
  {
    id: "e6",
    from: "sales@example.com",
    subject: "Opportunity #500123456 Rejected on SFDC",
    preview:
      "The opportunity #500123456 has been rejected on SFDC. Could you please check the reason for rejection and advise if we can resubmit with corrections?",
    time: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2), // 2 days ago
    status: "manual",
    read: false,
  },
  {
    id: "e7",
    from: "account-manager@example.com",
    subject: "Pending Approval on SFDC #500789012",
    preview:
      "Could you please approve the opportunity #500789012 pending with you for review on SFDC and push it to pricing. The customer is urgently waiting for the quote...",
    time: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3), // 3 days ago
    status: "replied",
    read: true,
  },
  {
    id: "e8",
    from: "customer@example.com",
    subject: "Unable to Get Quote Document for #500345678",
    preview:
      "We are unable to retrieve the quote document for #500345678 which shows as closed on GPMS. Could you please help us get the document as we need to place the order...",
    time: new Date(Date.now() - 1000 * 60 * 60 * 24 * 4), // 4 days ago
    status: "replied",
    read: true,
  },
]

export function EmailList({ filter, searchQuery, selectedEmail, onSelectEmail }: EmailListProps) {
  const filteredEmails = emails.filter((email) => {
    // Filter by status
    if (
      filter !== "all" &&
      ((filter === "new" && email.status !== "new") ||
        (filter === "replied" && email.status !== "replied") ||
        (filter === "manual" && email.status !== "manual"))
    ) {
      return false
    }

    // Filter by search query
    if (
      searchQuery &&
      !email.subject.toLowerCase().includes(searchQuery.toLowerCase()) &&
      !email.from.toLowerCase().includes(searchQuery.toLowerCase())
    ) {
      return false
    }

    return true
  })

  return (
    <div className="space-y-1">
      {filteredEmails.length === 0 ? (
        <div className="p-4 text-center text-muted-foreground">No emails found</div>
      ) : (
        filteredEmails.map((email) => (
          <div
            key={email.id}
            className={cn(
              "flex cursor-pointer flex-col gap-1 rounded-lg border p-3 transition-colors hover:bg-muted/50",
              selectedEmail === email.id && "bg-muted",
              !email.read && "border-l-4 border-l-primary",
            )}
            onClick={() => onSelectEmail(email.id)}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-medium">{email.from}</span>
                {email.status === "new" && (
                  <Badge
                    variant="outline"
                    className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
                  >
                    New
                  </Badge>
                )}
                {email.status === "replied" && (
                  <Badge
                    variant="outline"
                    className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                  >
                    Auto-Replied
                  </Badge>
                )}
                {email.status === "manual" && (
                  <Badge variant="outline" className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                    Manual Reply
                  </Badge>
                )}
              </div>
              <span className="text-xs text-muted-foreground">
                {formatDistanceToNow(email.time, { addSuffix: true })}
              </span>
            </div>
            <div className="font-medium">{email.subject}</div>
            <div className="text-sm text-muted-foreground line-clamp-1">{email.preview}</div>
          </div>
        ))
      )}
    </div>
  )
}

