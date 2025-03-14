"use client"

import { Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts"

import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { day: "Mon", auto: 2.4, manual: 12.8 },
  { day: "Tue", auto: 2.1, manual: 10.5 },
  { day: "Wed", auto: 2.5, manual: 14.2 },
  { day: "Thu", auto: 1.9, manual: 11.3 },
  { day: "Fri", auto: 2.2, manual: 13.7 },
  { day: "Sat", auto: 2.6, manual: 15.1 },
  { day: "Sun", auto: 2.3, manual: 12.9 },
]

export function ResponseTimeChart() {
  return (
    <ChartContainer
      config={{
        auto: {
          label: "Auto Reply (minutes)",
          color: "hsl(var(--chart-1))",
        },
        manual: {
          label: "Manual Reply (minutes)",
          color: "hsl(var(--chart-2))",
        },
      }}
      className="h-[200px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="day" />
          <YAxis />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Line type="monotone" dataKey="auto" strokeWidth={2} activeDot={{ r: 6 }} stroke="var(--color-auto)" />
          <Line type="monotone" dataKey="manual" strokeWidth={2} activeDot={{ r: 6 }} stroke="var(--color-manual)" />
        </LineChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}

