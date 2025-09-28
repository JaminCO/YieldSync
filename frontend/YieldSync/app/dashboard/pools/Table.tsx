import { poolsTableInfo } from "@/data/poolsTableInfo";
import React from "react";

const Table = () => {
	return (
		<div className="overflow-x-auto rounded-2xl w-[90%] mx-auto">
			<table className="hidden md:table min-w-full border-collapse  bg-[#070550]  ">
				<colgroup>
					<col className="w-[10%]" /> {/* Pool */}
					<col className="w-[15%]" /> {/* Estimated APY */}
					<col className="w-[15%]" /> {/* Risk Score */}
					<col className="w-[40%]" /> {/* Summary */}
					<col className="w-[10%]" /> {/* Action */}
				</colgroup>

				<thead className="bg-[#070550] text-white">
					<tr>
						<th className="px-6 py-3 text-left">Pool</th>
						<th className="px-6 py-3 text-left">Estimated APY</th>
						<th className="px-6 py-3 text-left">Risk Score</th>
						<th className="px-6 py-3 text-left">Summary</th>
						<th className="px-6 py-3 text-left">Action</th>
					</tr>
				</thead>

				<tbody>
					{poolsTableInfo.map((info) => (
						<tr key={info.id} className="border-t">
							<td className="px-6 py-4">{info.pool}</td>
							<td className="px-6 py-4">{info.estimatedAPY}%</td>
							<td className="px-6 py-4">{info.riskScore}</td>
							<td className="px-6 py-4">{info.summary}</td>
							<td className="px-6 py-4">
								<button className="bg-[#00a2ff] text-white px-4 py-2 rounded-3xl cursor-pointer">
									Invest
								</button>
							</td>
						</tr>
					))}
				</tbody>
			</table>

			{/* Mobile card view */}
			<div className="md:hidden space-y-4">
				{poolsTableInfo.map((info) => (
					<div
						key={info.id}
						className="bg-[#070550] text-white rounded-lg p-4 shadow"
					>
						<p>
							<span className="font-semibold">Pool:</span> {info.pool}
						</p>
						<p>
							<span className="font-semibold">Estimated APY:</span>{info.estimatedAPY}%
						</p>
						<p>
							<span className="font-semibold">Risk Score:</span> {info.riskScore}
						</p>
						<p>
							<span className="font-semibold">Summary:</span> {info.summary}
						</p>
						<button className="mt-3 bg-[#00a2ff] cursor-pointer text-white px-4 py-2 rounded">
							Invest
						</button>
					</div>
				))}
			</div>
		</div>
	);
};

export default Table;
