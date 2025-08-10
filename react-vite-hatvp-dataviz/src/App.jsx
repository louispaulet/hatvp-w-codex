import { useEffect, useMemo, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';

function App() {
  const [allData, setAllData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [topN, setTopN] = useState(10);

  useEffect(() => {
    d3.csv('/organization_mentions.csv', d => ({
      organization: d.organization,
      mentions: +d.mentions,
    })).then(csvData => {
      const filtered = csvData.filter(d => d.mentions > 0);
      setAllData(filtered);
    });
  }, []);

  const data = useMemo(() => {
    return allData
      .filter(d =>
        d.organization.toLowerCase().includes(searchTerm.toLowerCase()),
      )
      .sort((a, b) => b.mentions - a.mentions)
      .slice(0, topN);
  }, [allData, searchTerm, topN]);

  return (
    <div className="p-4 flex flex-col gap-4">
      <header>
        <h1 className="text-2xl font-bold">Top Organization Mentions</h1>
        <p className="text-sm text-gray-600">
          Explore which organizations are most frequently referenced in
          declarations.
        </p>
      </header>
      <div className="flex flex-wrap gap-4">
        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="search">
            Search
          </label>
          <input
            id="search"
            type="text"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="border rounded px-2 py-1"
            placeholder="Type a name..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="topn">
            Top N
          </label>
          <input
            id="topn"
            type="number"
            min="1"
            max="50"
            value={topN}
            onChange={e => setTopN(Math.max(1, Number(e.target.value)))}
            className="border rounded px-2 py-1 w-24"
          />
        </div>
      </div>
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

