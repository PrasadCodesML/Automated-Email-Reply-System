"use client"

import { formatDistanceToNow } from "date-fns"
import { MessageSquareWarning } from "lucide-react"

import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"

interface ManualReplyListProps {
  searchQuery: string
  selectedEmail: string | null
  onSelectEmail: (id: string) => void
}

const manualReplyEmails = [
  {
    id: "m1",
    from: "distributor@example.com",
    subject: "POS Replace Request - Complex Case",
    preview:
      "This is with regards to POS update on quote 500987654 to XYZ Manufacturing (new POS customer name). Upon checking we found potential conflicts with new POS customers...",
    time: new Date(Date.now() - 1000 * 60 * 15), // 15 minutes ago
    priority: "high",
  },
  {
    id: "m2",
    from: "enterprise@example.com",
    subject: "LOA Query - Missing Information",
    preview:
      "We received an LOA for agreement ABC789 but there are several missing details. The LOA doesn't specify the authorized part numbers and the validity period is unclear...",
    time: new Date(Date.now() - 1000 * 60 * 45), // 45 minutes ago
    priority: "high",
  },
  {
    id: "m3",
    from: "partner@example.com",
    subject: "S&D Claim Rejection Query",
    preview:
      "Our S&D claim #CL123456 was rejected and we need to understand the reason. The claim was for customer DEF Industries under agreement P000789...",
    time: new Date(Date.now() - 1000 * 60 * 90), // 1.5 hours ago
    priority: "medium",
  },
  {
    id: "m4",
    from: "customer@example.com",
    subject: "Agreement PN Addition Request",
    preview:
      "We need to add the following part numbers to our existing agreement ABC456: PN555, PN666, PN777. These parts are critical for our upcoming project...",
    time: new Date(Date.now() - 1000 * 60 * 180), // 3 hours ago
    priority: "medium",
  },
  {
    id: "m5",
    from: "sales@example.com",
    subject: "SFDC Opportunity Rejected Incorrectly",
    preview:
      "The opportunity #500654321 has been rejected on SFDC but we believe this was done incorrectly. The customer chain information was accurate...",
    time: new Date(Date.now() - 1000 * 60 * 240), // 4 hours ago
    priority: "high",
  },
  {
    id: "m6",
    from: "distributor@example.com",
    subject: "TE.com SPR Issue for Multiple PNs",
    preview:
      "Our customer is unable to raise SPRs on TE.com for the following part numbers: PN888, PN999, PN101. They've tried multiple times but keep getting error messages...",
    time: new Date(Date.now() - 1000 * 60 * 300), // 5 hours ago
    priority: "low",
  },
  {
    id: "m7",
    from: "account@example.com",
    subject: "Quote Routing Issue - Not Reaching GPMS",
    preview:
      "We raised quote #500333444 but it hasn't reached GPMS for pricing. The customer has been waiting for over a week and we need to expedite this...",
    time: new Date(Date.now() - 1000 * 60 * 360), // 6 hours ago
    priority: "medium",
  },
  {
    id: "m8",
    from: "partner@example.com",
    subject: "Piggyback Creation with Special Terms",
    preview:
      "We need to create a piggyback for distributor GHI with special pricing terms. This is linked to OEM agreement DEF789 and requires management approval...",
    time: new Date(Date.now() - 1000 * 60 * 420), // 7 hours ago
    priority: "high",
  },
]

export function ManualReplyList({ searchQuery, selectedEmail, onSelectEmail }: ManualReplyListProps) {
  const filteredEmails = manualReplyEmails.filter((email) => {
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
              email.priority === "high" && "border-l-4 border-l-red-500",
              email.priority === "medium" && "border-l-4 border-l-yellow-500",
              email.priority === "low" && "border-l-4 border-l-green-500",
            )}
            onClick={() => onSelectEmail(email.id)}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MessageSquareWarning className="h-4 w-4 text-blue-500" />
                <span className="font-medium">{email.from}</span>
                {email.priority === "high" && (
                  <Badge variant="outline" className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">
                    High Priority
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

