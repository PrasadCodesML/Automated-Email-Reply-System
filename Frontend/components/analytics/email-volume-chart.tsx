"use client"

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, XAxis, YAxis } from "recharts"

import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { date: "Jan", received: 120, replied: 100, manual: 20 },
  { date: "Feb", received: 145, replied: 125, manual: 20 },
  { date: "Mar", received: 160, replied: 140, manual: 20 },
  { date: "Apr", received: 190, replied: 160, manual: 30 },
  { date: "May", received: 210, replied: 180, manual: 30 },
  { date: "Jun", received: 250, replied: 210, manual: 40 },
  { date: "Jul", received: 280, replied: 240, manual: 40 },
]

export function EmailVolumeChart() {
  return (
    <ChartContainer
      config={{
        received: {
          label: "Received",
          color: "hsl(var(--chart-1))",
        },
        replied: {
          label: "Auto-Replied",
          color: "hsl(var(--chart-2))",
        },
        manual: {
          label: "Manual Replies",
          color: "hsl(var(--chart-3))",
        },
      }}
      className="h-[300px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Area
            type="monotone"
            dataKey="received"
            stackId="1"
            stroke="var(--color-received)"
            fill="var(--color-received)"
            fillOpacity={0.6}
          />
          <Area
            type="monotone"
            dataKey="replied"
            stackId="2"
            stroke="var(--color-replied)"
            fill="var(--color-replied)"
            fillOpacity={0.6}
          />
          <Area
            type="monotone"
            dataKey="manual"
            stackId="3"
            stroke="var(--color-manual)"
            fill="var(--color-manual)"
            fillOpacity={0.6}
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}

