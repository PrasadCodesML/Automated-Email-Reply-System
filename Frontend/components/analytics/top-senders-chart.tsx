"use client"

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

const data = [
  { name: "distributor-a.com", count: 87 },
  { name: "oem-partner.com", count: 65 },
  { name: "supplier-b.com", count: 54 },
  { name: "customer-c.com", count: 42 },
  { name: "vendor-d.com", count: 38 },
]

export function TopSendersChart() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis type="category" dataKey="name" width={100} />
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

