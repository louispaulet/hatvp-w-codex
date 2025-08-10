import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';

function DelayByMandate() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/mandate_delay_median.csv', d => ({
      mandate_type: d.mandate_type,
      delay_days: +d.delay_days,
    })).then(setData);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold">Median Publication Delay by Mandate</h1>
      <p className="text-sm text-gray-600 mb-4">
        Median days between deposit and publication.
      </p>
      <div className="w-full h-96">
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="mandate_type" angle={-45} textAnchor="end" height={120} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="delay_days" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default DelayByMandate;
