import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function JobTrendsChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-800 border-2 border-red-500">
        <p className="text-red-400 font-mono font-bold">
          [ NO_DATA_AVAILABLE ]
        </p>
      </div>
    );
  }

  // Format data for the chart
  const chartData = data.map((item) => ({
    week: new Date(item.week_starting).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "2-digit",
    }),
    fullDate: item.week_starting,
    "Total DE": item.data_engineer,
    Junior: item.junior_data_engineer,
    Senior: item.senior_data_engineer,
  }));

  // Custom tooltip with 8-bit aesthetic
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-black border-2 border-green-500 p-3 font-mono text-sm shadow-lg">
          <p className="text-green-400 font-bold mb-2">[ {label} ]</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="mb-1">
              {entry.name}: {entry.value} jobs
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  // Custom legend with 8-bit style
  const CustomLegend = (props) => {
    const { payload } = props;
    return (
      <div className="flex justify-center gap-6 mt-4 flex-wrap">
        {payload.map((entry, index) => (
          <div
            key={index}
            className="flex items-center gap-2 font-mono text-sm"
          >
            <div
              className="w-4 h-4 border-2"
              style={{
                backgroundColor: entry.color,
                borderColor: entry.color,
              }}
            />
            <span style={{ color: entry.color }} className="font-bold">
              [ {entry.value} ]
            </span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="w-full">
      <ResponsiveContainer width="100%" height={500}>
        <LineChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis
            dataKey="week"
            stroke="#9CA3AF"
            tick={{ fill: "#9CA3AF", fontFamily: "monospace", fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            stroke="#9CA3AF"
            tick={{ fill: "#9CA3AF", fontFamily: "monospace", fontSize: 12 }}
            label={{
              value: "ACTIVE_POSTINGS",
              angle: -90,
              position: "insideLeft",
              style: {
                fill: "#9CA3AF",
                fontFamily: "monospace",
                fontSize: 12,
                fontWeight: "bold",
              },
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend content={<CustomLegend />} />
          <Line
            type="monotone"
            dataKey="Total DE"
            stroke="#60A5FA"
            strokeWidth={3}
            dot={{
              r: 4,
              fill: "#60A5FA",
              strokeWidth: 2,
              stroke: "#1E3A8A",
            }}
            activeDot={{
              r: 6,
              fill: "#60A5FA",
              strokeWidth: 3,
              stroke: "#1E3A8A",
            }}
          />
          <Line
            type="monotone"
            dataKey="Junior"
            stroke="#34D399"
            strokeWidth={3}
            dot={{
              r: 4,
              fill: "#34D399",
              strokeWidth: 2,
              stroke: "#065F46",
            }}
            activeDot={{
              r: 6,
              fill: "#34D399",
              strokeWidth: 3,
              stroke: "#065F46",
            }}
          />
          <Line
            type="monotone"
            dataKey="Senior"
            stroke="#FBBF24"
            strokeWidth={3}
            dot={{
              r: 4,
              fill: "#FBBF24",
              strokeWidth: 2,
              stroke: "#78350F",
            }}
            activeDot={{
              r: 6,
              fill: "#FBBF24",
              strokeWidth: 3,
              stroke: "#78350F",
            }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
