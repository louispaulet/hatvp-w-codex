import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/organization_mentions.csv', d => ({
      organization: d.organization,
      mentions: +d.mentions,
    })).then(csvData => {
      const filtered = csvData
        .filter(d => d.mentions > 0)
        .sort((a, b) => b.mentions - a.mentions)
        .slice(0, 10);
      setData(filtered);
    });
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Top Organization Mentions</h1>
      <div className="w-full h-96">
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="organization" angle={-45} textAnchor="end" height={120} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="mentions" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;

