import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';

const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#facc15'];

function GenderDistribution() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/gender_counts.csv', d => ({
      gender: d.gender,
      count: +d.count,
    })).then(setData);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold">Gender Distribution</h1>
      <p className="text-sm text-gray-600 mb-4">
        Gender identities among declarants.
      </p>
      <div className="w-full h-96">
        <ResponsiveContainer>
          <PieChart>
            <Pie data={data} dataKey="count" nameKey="gender" outerRadius={120} label>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default GenderDistribution;
