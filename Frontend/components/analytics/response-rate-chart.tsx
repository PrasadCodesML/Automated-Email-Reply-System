"use client"

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, XAxis, YAxis } from "recharts"

import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { name: "POS Replace", auto: 85, manual: 15 },
  { name: "General Pricing", auto: 70, manual: 30 },
  { name: "Piggyback", auto: 60, manual: 40 },
  { name: "Ship & Debit", auto: 75, manual: 25 },
  { name: "SFDC Issues", auto: 65, manual: 35 },
]

export function ResponseRateChart() {
  return (
    <ChartContainer
      config={{
        auto: {
          label: "Auto Replies (%)",
          color: "hsl(var(--chart-1))",
        },
        manual: {
          label: "Manual Replies (%)",
          color: "hsl(var(--chart-2))",
        },
      }}
      className="h-[300px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Bar dataKey="auto" stackId="a" fill="var(--color-auto)" />
          <Bar dataKey="manual" stackId="a" fill="var(--color-manual)" />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}

