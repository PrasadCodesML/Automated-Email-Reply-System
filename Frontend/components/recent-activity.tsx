import { formatDistanceToNow } from "date-fns"
import { Check, Clock, Mail, MessageSquareIcon as MessageSquareCheck } from "lucide-react"

import { cn } from "@/lib/utils"

const activities = [
  {
    id: "1",
    email: "customer@example.com",
    subject: "Order Confirmation #12345",
    type: "auto-reply",
    time: new Date(Date.now() - 1000 * 60 * 5), // 5 minutes ago
  },
  {
    id: "2",
    email: "job-applicant@example.com",
    subject: "Application for Senior Developer Position",
    type: "manual-reply",
    time: new Date(Date.now() - 1000 * 60 * 25), // 25 minutes ago
  },
  {
    id: "3",
    email: "partner@example.com",
    subject: "Partnership Opportunity",
    type: "new",
    time: new Date(Date.now() - 1000 * 60 * 40), // 40 minutes ago
  },
  {
    id: "4",
    email: "support-request@example.com",
    subject: "Help with Account Access",
    type: "auto-reply",
    time: new Date(Date.now() - 1000 * 60 * 120), // 2 hours ago
  },
]

export function RecentActivity() {
  return (
    <div className="space-y-4">
      {activities.map((activity) => (
        <div key={activity.id} className="flex items-start gap-4">
          <div
            className={cn(
              "mt-0.5 rounded-full p-1",
              activity.type === "auto-reply" && "bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400",
              activity.type === "manual-reply" && "bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400",
              activity.type === "new" && "bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400",
            )}
          >
            {activity.type === "auto-reply" && <MessageSquareCheck className="h-4 w-4" />}
            {activity.type === "manual-reply" && <Check className="h-4 w-4" />}
            {activity.type === "new" && <Mail className="h-4 w-4" />}
          </div>
          <div className="flex-1 space-y-1">
            <p className="text-sm font-medium leading-none">{activity.subject}</p>
            <p className="text-sm text-muted-foreground">{activity.email}</p>
          </div>
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Clock className="h-3 w-3" />
            <span>{formatDistanceToNow(activity.time, { addSuffix: true })}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

