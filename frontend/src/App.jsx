import { useEffect, useState } from "react";
import { supabase } from "./lib/supabase";
import JobTrendsChart from "./components/JobTrendsChart";
import StatsCards from "./components/StatsCards";

function App() {
  const [jobData, setJobData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJobData();
  }, []);

  async function fetchJobData() {
    try {
      setLoading(true);

      // Calculate date 1 year ago
      const oneYearAgo = new Date();
      oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
      const oneYearAgoStr = oneYearAgo.toISOString().split("T")[0];

      const { data, error } = await supabase
        .from("job_counts")
        .select("*")
        .eq("location", "Berlin, Germany")
        .gte("week_starting", oneYearAgoStr)
        .order("week_starting", { ascending: false });

      if (error) throw error;

      setJobData(data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-gray-700 border-t-green-500"></div>
          <p className="mt-4 text-green-400 font-mono text-lg">
            LOADING DATA...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        <div className="bg-red-900 border-2 border-red-500 rounded-none p-6 max-w-md font-mono">
          <h2 className="text-red-300 font-bold text-xl mb-2">[ ERROR ]</h2>
          <p className="text-red-200 mb-4">{error}</p>
          <button
            onClick={fetchJobData}
            className="bg-red-700 text-white px-4 py-2 border-2 border-red-500 hover:bg-red-600 transition font-bold"
          >
            &gt; RETRY
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-green-400">
      {/* Header */}
      <header className="bg-black border-b-4 border-green-500 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-4xl font-bold font-mono text-green-400 mb-2 tracking-wider">
                &gt; BERNALYTICS_
              </h1>
              <p className="text-sm text-gray-400 font-mono">
                Berlin Data Engineering Job Market Monitor
              </p>
            </div>
            <button
              onClick={fetchJobData}
              className="bg-green-700 text-black px-6 py-3 border-2 border-green-500 hover:bg-green-600 transition font-mono font-bold tracking-wider shadow-lg hover:shadow-green-500/50"
            >
              &gt; REFRESH_DATA
            </button>
          </div>
        </div>
      </header>

      {/* Info Banner */}
      <div className="bg-gray-800 border-b-2 border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="font-mono text-sm">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-900 border border-green-500 p-3">
                <span className="text-green-500 font-bold">
                  [ DATA SOURCE ]
                </span>
                <p className="text-gray-300 mt-1">Google Search via SERP API</p>
                <p className="text-gray-500 text-xs mt-1">
                  linkedin.com/jobs Berlin postings
                </p>
              </div>
              <div className="bg-gray-900 border border-blue-500 p-3">
                <span className="text-blue-400 font-bold">
                  [ ACTIVE POSTINGS ]
                </span>
                <p className="text-gray-300 mt-1">Live job counts per week</p>
                <p className="text-gray-500 text-xs mt-1">
                  Updated every Monday 9AM UTC
                </p>
              </div>
              <div className="bg-gray-900 border border-yellow-500 p-3">
                <span className="text-yellow-400 font-bold">
                  [ TIME RANGE ]
                </span>
                <p className="text-gray-300 mt-1">Past 12 months</p>
                <p className="text-gray-500 text-xs mt-1">
                  Weekly snapshots of job market
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {jobData.length === 0 ? (
          <div className="bg-yellow-900 border-2 border-yellow-500 p-8 text-center font-mono">
            <p className="text-yellow-300 text-lg font-bold mb-2">
              [ NO DATA AVAILABLE ]
            </p>
            <p className="text-yellow-200">
              Run the data collection script to populate the dashboard.
            </p>
            <p className="text-yellow-500 text-sm mt-2">
              python -m bernalytics.main --write-to-db
            </p>
          </div>
        ) : (
          <>
            <StatsCards data={jobData} />

            {/* Chart Section */}
            <div className="mb-8">
              <div className="bg-gray-800 border-2 border-green-500 p-1 mb-2">
                <div className="bg-gray-900 p-4">
                  <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                    <h2 className="text-2xl font-bold font-mono text-green-400 tracking-wider">
                      [ TIME_SERIES_ANALYSIS ]
                    </h2>
                    <div className="text-xs text-gray-500 font-mono">
                      DISPLAYING: {jobData.length} WEEKS
                    </div>
                  </div>
                  <p className="text-sm text-gray-400 font-mono mb-4 leading-relaxed">
                    &gt; Each data point represents the number of{" "}
                    <span className="text-green-400">active job postings</span>{" "}
                    found that week.
                    <br />
                    &gt; Data collected weekly via automated Google Search of
                    LinkedIn job listings.
                    <br />
                    &gt; Trend shows market demand over time for different
                    experience levels.
                  </p>
                  <JobTrendsChart data={[...jobData].reverse()} />
                </div>
              </div>
            </div>

            {/* Data Table */}
            <div className="bg-gray-800 border-2 border-blue-500 overflow-hidden">
              <div className="bg-gray-900 px-6 py-4 border-b-2 border-blue-500">
                <h2 className="text-2xl font-bold font-mono text-blue-400 tracking-wider">
                  [ WEEKLY_DATA_LOG ]
                </h2>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y-2 divide-gray-700 font-mono">
                  <thead className="bg-black">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-bold text-green-400 uppercase tracking-wider border-r border-gray-700">
                        WEEK_START
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-blue-400 uppercase tracking-wider border-r border-gray-700">
                        TOTAL_DE
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-green-400 uppercase tracking-wider border-r border-gray-700">
                        JUNIOR
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider border-r border-gray-700">
                        SENIOR
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-purple-400 uppercase tracking-wider">
                        SUM
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-gray-900 divide-y divide-gray-800">
                    {jobData.map((row, idx) => (
                      <tr
                        key={row.id}
                        className={`hover:bg-gray-800 transition ${idx === 0 ? "bg-gray-800" : ""}`}
                      >
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300 border-r border-gray-800">
                          {new Date(row.week_starting).toLocaleDateString(
                            "en-US",
                            {
                              year: "numeric",
                              month: "short",
                              day: "numeric",
                            },
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-400 border-r border-gray-800">
                          {row.data_engineer}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-green-400 border-r border-gray-800">
                          {row.junior_data_engineer}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-yellow-400 border-r border-gray-800">
                          {row.senior_data_engineer}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-purple-400">
                          {row.data_engineer +
                            row.junior_data_engineer +
                            row.senior_data_engineer}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 bg-black border-t-4 border-green-500">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="text-center font-mono text-sm">
            <p className="text-gray-500 mb-2">[ SYSTEM_INFO ]</p>
            <p className="text-gray-400">
              AUTO_UPDATE: Monday 09:00 UTC
              {jobData.length > 0 && (
                <>
                  {" · "}
                  LAST_SYNC:{" "}
                  {new Date(jobData[0].collected_at).toLocaleString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </>
              )}
            </p>
            <p className="text-gray-600 text-xs mt-2">
              &gt; Data powered by SERP_API · Stored in SUPABASE · Built with
              REACT
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
