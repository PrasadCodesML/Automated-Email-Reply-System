import Link from "next/link"
import { ArrowRight, Mail, MessageSquareIcon as MessageSquareCheck, MessageSquareWarning } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { EmailAccountCard } from "@/components/email-account-card"
import { RecentActivity } from "@/components/recent-activity"
import { ResponseTimeChart } from "@/components/response-time-chart"

export default function Dashboard() {
  const emailAccounts = [
    {
      id: "1",
      email: "support@company.com",
      newEmails: 24,
      repliedEmails: 156,
      manualReplies: 8,
    },
    {
      id: "2",
      email: "sales@company.com",
      newEmails: 12,
      repliedEmails: 98,
      manualReplies: 3,
    },
    {
      id: "3",
      email: "info@company.com",
      newEmails: 31,
      repliedEmails: 203,
      manualReplies: 15,
    },
    {
      id: "4",
      email: "careers@company.com",
      newEmails: 7,
      repliedEmails: 42,
      manualReplies: 2,
    },
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="flex h-16 items-center px-4 gap-4">
          <SidebarTrigger />
          <h1 className="text-xl font-semibold">Dashboard</h1>
        </div>
      </header>
      <div className="flex-1 space-y-6 p-6">
        <div className="grid gap-6 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Emails</CardTitle>
              <Mail className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1,248</div>
              <p className="text-xs text-muted-foreground">+12% from last month</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Auto-Replied</CardTitle>
              <MessageSquareCheck className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">924</div>
              <p className="text-xs text-muted-foreground">74% of total emails</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Manual Replies</CardTitle>
              <MessageSquareWarning className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">76</div>
              <p className="text-xs text-muted-foreground">6% of total emails</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card className="col-span-2 md:col-span-1">
            <CardHeader>
              <CardTitle>Response Time</CardTitle>
              <CardDescription>Average response time over the last 30 days</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponseTimeChart />
            </CardContent>
          </Card>
          <Card className="col-span-2 md:col-span-1">
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>Latest email activities across all accounts</CardDescription>
            </CardHeader>
            <CardContent>
              <RecentActivity />
            </CardContent>
          </Card>
        </div>

        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Email Accounts</h2>
            <Button variant="outline" size="sm" asChild>
              <Link href="/email">
                View All <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>

          <Tabs defaultValue="all" className="w-full">
            <TabsList className="mb-4">
              <TabsTrigger value="all">All Accounts</TabsTrigger>
              <TabsTrigger value="active">
                Active <Badge className="ml-2 bg-green-500">3</Badge>
              </TabsTrigger>
              <TabsTrigger value="pending">
                Pending <Badge className="ml-2">1</Badge>
              </TabsTrigger>
            </TabsList>
            <TabsContent value="all" className="mt-0">
              <div className="grid gap-4 md:grid-cols-2">
                {emailAccounts.map((account) => (
                  <EmailAccountCard key={account.id} account={account} />
                ))}
              </div>
            </TabsContent>
            <TabsContent value="active" className="mt-0">
              <div className="grid gap-4 md:grid-cols-2">
                {emailAccounts.slice(0, 3).map((account) => (
                  <EmailAccountCard key={account.id} account={account} />
                ))}
              </div>
            </TabsContent>
            <TabsContent value="pending" className="mt-0">
              <div className="grid gap-4 md:grid-cols-2">
                {emailAccounts.slice(3, 4).map((account) => (
                  <EmailAccountCard key={account.id} account={account} />
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}

