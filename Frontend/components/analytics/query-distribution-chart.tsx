"use client"

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

const data = [
  { name: "POS Replace", count: 42 },
  { name: "General Pricing", count: 68 },
  { name: "Piggyback Creation", count: 35 },
  { name: "Adding Parts", count: 29 },
  { name: "Ship & Debit", count: 45 },
  { name: "SFDC Rejections", count: 22 },
  { name: "Pending Approval", count: 38 },
  { name: "Quote Document", count: 19 },
  { name: "Quote Routing", count: 15 },
  { name: "Customer Data", count: 31 },
  { name: "GPMS Review", count: 27 },
  { name: "SFDC Review", count: 33 },
  { name: "LOA Queries", count: 24 },
  { name: "S&D Claim", count: 18 },
  { name: "Agreement PN", count: 21 },
  { name: "TE.com SPR", count: 17 },
]

export function QueryDistributionChart() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 11 }} />
          <Tooltip
            formatter={(value) => [`${value} emails`, "Count"]}
            contentStyle={{
              backgroundColor: "var(--background)",
              borderColor: "var(--border)",
              borderRadius: "0.5rem",
              boxShadow: "var(--shadow)",
            }}
          />
          <Bar dataKey="count" fill="hsl(var(--primary))" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

