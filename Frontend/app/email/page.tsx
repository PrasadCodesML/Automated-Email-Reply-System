"use client"

import { useState } from "react"
import { useSearchParams } from "next/navigation"
import { Filter, Mail, MessageSquareIcon as MessageSquareCheck, MessageSquareWarning, Search } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { EmailList } from "@/components/email/email-list"
import { EmailDetail } from "@/components/email/email-detail"

export default function EmailPage() {
  const searchParams = useSearchParams()
  const accountId = searchParams.get("account")
  const [selectedEmail, setSelectedEmail] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="flex h-16 items-center px-4 gap-4">
          <SidebarTrigger />
          <h1 className="text-xl font-semibold">Email</h1>
          {accountId && (
            <Badge variant="outline" className="ml-2">
              Account:{" "}
              {accountId === "1"
                ? "support@company.com"
                : accountId === "2"
                  ? "sales@company.com"
                  : accountId === "3"
                    ? "info@company.com"
                    : "careers@company.com"}
            </Badge>
          )}
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
            <Button variant="outline" size="icon">
              <Filter className="h-4 w-4" />
              <span className="sr-only">Filter</span>
            </Button>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        <div className="w-full md:w-1/3 border-r">
          <div className="p-4">
            <Tabs defaultValue="all">
              <TabsList className="grid grid-cols-4 mb-4">
                <TabsTrigger value="all">
                  All
                  <Badge className="ml-2">248</Badge>
                </TabsTrigger>
                <TabsTrigger value="new">
                  <Mail className="mr-1 h-4 w-4" />
                  New
                  <Badge className="ml-2">74</Badge>
                </TabsTrigger>
                <TabsTrigger value="replied">
                  <MessageSquareCheck className="mr-1 h-4 w-4" />
                  Replied
                  <Badge className="ml-2">156</Badge>
                </TabsTrigger>
                <TabsTrigger value="manual">
                  <MessageSquareWarning className="mr-1 h-4 w-4" />
                  Manual
                  <Badge className="ml-2">18</Badge>
                </TabsTrigger>
              </TabsList>

              <TabsContent value="all" className="m-0">
                <EmailList
                  filter="all"
                  searchQuery={searchQuery}
                  selectedEmail={selectedEmail}
                  onSelectEmail={setSelectedEmail}
                />
              </TabsContent>
              <TabsContent value="new" className="m-0">
                <EmailList
                  filter="new"
                  searchQuery={searchQuery}
                  selectedEmail={selectedEmail}
                  onSelectEmail={setSelectedEmail}
                />
              </TabsContent>
              <TabsContent value="replied" className="m-0">
                <EmailList
                  filter="replied"
                  searchQuery={searchQuery}
                  selectedEmail={selectedEmail}
                  onSelectEmail={setSelectedEmail}
                />
              </TabsContent>
              <TabsContent value="manual" className="m-0">
                <EmailList
                  filter="manual"
                  searchQuery={searchQuery}
                  selectedEmail={selectedEmail}
                  onSelectEmail={setSelectedEmail}
                />
              </TabsContent>
            </Tabs>
          </div>
        </div>

        <div className="hidden md:block md:flex-1">
          {selectedEmail ? (
            <EmailDetail emailId={selectedEmail} />
          ) : (
            <div className="flex h-full items-center justify-center">
              <Card className="mx-auto max-w-md">
                <CardHeader>
                  <CardTitle>No Email Selected</CardTitle>
                  <CardDescription>Select an email from the list to view its details</CardDescription>
                </CardHeader>
                <CardContent className="flex justify-center">
                  <Mail className="h-16 w-16 text-muted-foreground/50" />
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

