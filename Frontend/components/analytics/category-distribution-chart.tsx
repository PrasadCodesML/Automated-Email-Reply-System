"use client"

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts"

const data = [
  { name: "POS Replace", value: 42 },
  { name: "General Pricing", value: 68 },
  { name: "Piggyback Creation", value: 35 },
  { name: "Adding Parts to Piggyback", value: 29 },
  { name: "Ship & Debit", value: 45 },
  { name: "SFDC Rejections", value: 22 },
  { name: "Pending Approval", value: 38 },
  { name: "Quote Document Issues", value: 19 },
  { name: "Quote Routing Issues", value: 15 },
  { name: "Customer Data Enquiries", value: 31 },
  { name: "GPMS Review Pending", value: 27 },
  { name: "SFDC Review Pending", value: 33 },
  { name: "LOA Queries", value: 24 },
  { name: "S&D Claim Rejection", value: 18 },
  { name: "Agreement PN Issues", value: 21 },
  { name: "TE.com SPR Issues", value: 17 },
]

// Generate colors dynamically based on the number of data items
const generateColors = (count) => {
  const baseColors = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#8884D8",
    "#82ca9d",
    "#ffc658",
    "#8dd1e1",
    "#a4de6c",
    "#d0ed57",
    "#83a6ed",
    "#8884d8",
    "#ffc658",
    "#ff8042",
    "#0088FE",
    "#00C49F",
  ]

  return baseColors.slice(0, count)
}

const COLORS = generateColors(data.length)

export function CategoryDistributionChart() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => (percent > 0.05 ? `${name}: ${(percent * 100).toFixed(0)}%` : "")}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value) => [`${value} emails`, "Count"]}
            contentStyle={{
              backgroundColor: "var(--background)",
              borderColor: "var(--border)",
              borderRadius: "0.5rem",
              boxShadow: "var(--shadow)",
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

