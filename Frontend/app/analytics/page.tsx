import { SidebarTrigger } from "@/components/ui/sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { CategoryDistributionChart } from "@/components/analytics/category-distribution-chart"
import { ResponseRateChart } from "@/components/analytics/response-rate-chart"
import { EmailVolumeChart } from "@/components/analytics/email-volume-chart"
import { TopSendersChart } from "@/components/analytics/top-senders-chart"
import { QueryDistributionChart } from "@/components/analytics/query-distribution-chart"

export default function AnalyticsPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="flex h-16 items-center px-4 gap-4">
          <SidebarTrigger />
          <h1 className="text-xl font-semibold">Analytics</h1>
        </div>
      </header>
      <div className="flex-1 space-y-6 p-6">
        <Tabs defaultValue="week" className="w-full">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Email Analytics</h2>
            <TabsList>
              <TabsTrigger value="day">Day</TabsTrigger>
              <TabsTrigger value="week">Week</TabsTrigger>
              <TabsTrigger value="month">Month</TabsTrigger>
              <TabsTrigger value="year">Year</TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value="day" className="mt-0 space-y-6">
            <AnalyticsContent />
          </TabsContent>
          <TabsContent value="week" className="mt-0 space-y-6">
            <AnalyticsContent />
          </TabsContent>
          <TabsContent value="month" className="mt-0 space-y-6">
            <AnalyticsContent />
          </TabsContent>
          <TabsContent value="year" className="mt-0 space-y-6">
            <AnalyticsContent />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

function AnalyticsContent() {
  return (
    <>
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="col-span-2 md:col-span-1">
          <CardHeader>
            <CardTitle>Email Categories</CardTitle>
            <CardDescription>Distribution of emails by category</CardDescription>
          </CardHeader>
          <CardContent>
            <CategoryDistributionChart />
          </CardContent>
        </Card>
        <Card className="col-span-2 md:col-span-1">
          <CardHeader>
            <CardTitle>Response Rate</CardTitle>
            <CardDescription>Auto vs. manual response rates</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponseRateChart />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Email Volume</CardTitle>
          <CardDescription>Email volume over time</CardDescription>
        </CardHeader>
        <CardContent>
          <EmailVolumeChart />
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="col-span-2 md:col-span-1">
          <CardHeader>
            <CardTitle>Top Senders</CardTitle>
            <CardDescription>Most frequent email senders</CardDescription>
          </CardHeader>
          <CardContent>
            <TopSendersChart />
          </CardContent>
        </Card>
        <Card className="col-span-2 md:col-span-1">
          <CardHeader>
            <CardTitle>Query Distribution</CardTitle>
            <CardDescription>Distribution of emails by query type</CardDescription>
          </CardHeader>
          <CardContent>
            <QueryDistributionChart />
          </CardContent>
        </Card>
      </div>
    </>
  )
}

