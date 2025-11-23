export default function StatsCards({ data }) {
  if (!data || data.length === 0) {
    return null
  }

  // Get the most recent week's data
  const latestData = data[0]

  // Calculate week-over-week change if we have previous data
  const previousData = data[1]
  const calculateChange = (current, previous) => {
    if (!previous) return null
    const change = current - previous
    const percentChange = ((change / previous) * 100).toFixed(1)
    return { change, percentChange }
  }

  const stats = [
    {
      title: 'Total Data Engineer',
      value: latestData.data_engineer,
      change: previousData ? calculateChange(latestData.data_engineer, previousData.data_engineer) : null,
      color: 'blue',
    },
    {
      title: 'Junior Positions',
      value: latestData.junior_data_engineer,
      change: previousData ? calculateChange(latestData.junior_data_engineer, previousData.junior_data_engineer) : null,
      color: 'green',
    },
    {
      title: 'Senior Positions',
      value: latestData.senior_data_engineer,
      change: previousData ? calculateChange(latestData.senior_data_engineer, previousData.senior_data_engineer) : null,
      color: 'amber',
    },
  ]

  const colorClasses = {
    blue: 'bg-blue-100 text-blue-800',
    green: 'bg-green-100 text-green-800',
    amber: 'bg-amber-100 text-amber-800',
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
            {stat.title}
          </h3>
          <div className="mt-2 flex items-baseline">
            <p className="text-4xl font-bold text-gray-900">{stat.value}</p>
            {stat.change && (
              <span
                className={`ml-2 text-sm font-medium ${
                  stat.change.change >= 0 ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {stat.change.change >= 0 ? '+' : ''}
                {stat.change.change} ({stat.change.percentChange}%)
              </span>
            )}
          </div>
          <div className="mt-4">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${colorClasses[stat.color]}`}>
              Week of {new Date(latestData.week_starting).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}
