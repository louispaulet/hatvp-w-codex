import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';

function AgeDistribution() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/age_band_counts.csv', d => ({
      age_band: d.age_band,
      count: +d.count,
    })).then(setData);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold">Declarant Age Distribution</h1>
      <p className="text-sm text-gray-600 mb-4">
        Age bands among declarants.
      </p>
      <div className="w-full h-96">
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="age_band" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default AgeDistribution;
