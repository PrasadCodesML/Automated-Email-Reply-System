import Link from "next/link"
import { ArrowRight, Mail } from "lucide-react"

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface EmailAccountCardProps {
  account: {
    id: string
    email: string
    newEmails: number
    repliedEmails: number
    manualReplies: number
  }
}

export function EmailAccountCard({ account }: EmailAccountCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Mail className="h-5 w-5" />
          {account.email}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-4">
          <div className="flex flex-col">
            <span className="text-sm text-muted-foreground">New</span>
            <span className="text-2xl font-bold">{account.newEmails}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-sm text-muted-foreground">Replied</span>
            <span className="text-2xl font-bold">{account.repliedEmails}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-sm text-muted-foreground">Manual</span>
            <span className="text-2xl font-bold">{account.manualReplies}</span>
          </div>
        </div>
      </CardContent>
      <CardFooter>
        <Button variant="ghost" size="sm" className="w-full" asChild>
          <Link href={`/email?account=${account.id}`}>
            Show More <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </Button>
      </CardFooter>
    </Card>
  )
}

