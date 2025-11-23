export default function StatsCards({ data }) {
  if (!data || data.length === 0) {
    return null;
  }

  // Get the most recent week's data
  const latestData = data[0];

  // Calculate week-over-week change if we have previous data
  const previousData = data[1];
  const calculateChange = (current, previous) => {
    if (!previous) return null;
    const change = current - previous;
    const percentChange = ((change / previous) * 100).toFixed(1);
    return { change, percentChange };
  };

  const stats = [
    {
      title: "TOTAL_DATA_ENGINEER",
      label: "All DE Positions",
      value: latestData.data_engineer,
      change: previousData
        ? calculateChange(latestData.data_engineer, previousData.data_engineer)
        : null,
      color: "blue",
      borderColor: "border-blue-500",
      textColor: "text-blue-400",
      bgColor: "bg-blue-900",
    },
    {
      title: "JUNIOR_POSITIONS",
      label: "Entry Level",
      value: latestData.junior_data_engineer,
      change: previousData
        ? calculateChange(
            latestData.junior_data_engineer,
            previousData.junior_data_engineer,
          )
        : null,
      color: "green",
      borderColor: "border-green-500",
      textColor: "text-green-400",
      bgColor: "bg-green-900",
    },
    {
      title: "SENIOR_POSITIONS",
      label: "Experienced",
      value: latestData.senior_data_engineer,
      change: previousData
        ? calculateChange(
            latestData.senior_data_engineer,
            previousData.senior_data_engineer,
          )
        : null,
      color: "yellow",
      borderColor: "border-yellow-500",
      textColor: "text-yellow-400",
      bgColor: "bg-yellow-900",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {stats.map((stat, index) => (
        <div
          key={index}
          className={`bg-gray-800 border-2 ${stat.borderColor} p-1 shadow-lg hover:shadow-xl transition-shadow`}
        >
          <div className="bg-gray-900 p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3
                  className={`text-xs font-bold ${stat.textColor} uppercase tracking-wider font-mono mb-1`}
                >
                  [ {stat.title} ]
                </h3>
                <p className="text-gray-500 text-xs font-mono">{stat.label}</p>
              </div>
              <div
                className={`w-3 h-3 ${stat.bgColor} border-2 ${stat.borderColor} animate-pulse`}
              />
            </div>

            <div className="mb-4">
              <p
                className={`text-5xl font-bold ${stat.textColor} font-mono tracking-wider`}
              >
                {stat.value}
              </p>
              <p className="text-gray-600 text-xs font-mono mt-1">
                ACTIVE_JOBS
              </p>
            </div>

            {stat.change && (
              <div
                className={`border-t-2 ${stat.borderColor} pt-4 font-mono text-sm`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-gray-500 text-xs">WoW CHANGE:</span>
                  <span
                    className={`font-bold ${
                      stat.change.change >= 0
                        ? "text-green-400"
                        : "text-red-400"
                    }`}
                  >
                    {stat.change.change >= 0 ? "▲ +" : "▼ "}
                    {stat.change.change} ({stat.change.percentChange}%)
                  </span>
                </div>
              </div>
            )}

            <div className="mt-4 pt-4 border-t border-gray-700">
              <p className="text-gray-600 text-xs font-mono">
                WEEK_OF:{" "}
                {new Date(latestData.week_starting).toLocaleDateString(
                  "en-US",
                  {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  },
                )}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
