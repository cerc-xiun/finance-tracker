function StatCard({ label, badge, badgeClass, amount }) {
    return (
        <article className='stat-card'>
            <div className='stat-card__info'>
                <span className='stat-card__label'>{label}</span>
                <span className='stat-card__amount'>{amount}</span>
            </div>
            <span className={`stat-badge ${badgeClass}`}>{badge}</span>
        </article>
    )
}

export default function StatCards({ summary }) {
    const income = Number(summary?.total_income || 0)
    const expense = Number(summary?.total_expenses || 0)
    const net = Number(summary?.net_savings || 0)

    const netBadge = net >= 0 ? 'SURPLUS' : 'DEFICIT'
    const netBadgeClass = net >= 0 ? 'stat-badge--surplus' : 'stat-badge--deficit'

    const fmt = (value) =>
        value.toLocaleString('en-PH', {
            style: 'currency',
            currency: 'PHP',
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        });

    return (
        <header className='metrics-row'>
            <StatCard label="Total Income" badge="INFLOW" badgeClass='stat-badge--income' amount={fmt(income)} />
            <StatCard label="Total Expenses" badge="OUTFLOW" badgeClass='stat-badge--expense' amount={fmt(expense)} />
            <StatCard label="Net Savings" badge={netBadge} badgeClass={netBadgeClass} amount={fmt(net)} />
        </header>
    )
}