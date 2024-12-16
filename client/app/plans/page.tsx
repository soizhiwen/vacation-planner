import Link from 'next/link';
import { notFound } from 'next/navigation';
import { readPlans } from '@/app/lib/actions';
import { DeletePlan } from '@/app/ui/plans/buttons';
import { Plans, PlanWithHeader } from '@/app/lib/definitions';

export default async function Page(props: {
  searchParams?: Promise<{
    limit?: string;
  }>;
}) {
  const searchParams = await props.searchParams;
  const limit = Number(searchParams?.limit) || 10;
  const plans: Plans = await readPlans(limit);

  if (plans.length === 0) {
    notFound();
  }

  return (
    <div>
      {plans &&
        plans.map((plan: PlanWithHeader) => (
          <div key={plan._id}>
            <div>
              <Link href={`/plans/${plan._id}`}>
                {plan.title}
              </Link>
              <p>
                {plan.description}
              </p>
            </div>
            <DeletePlan
              id={plan._id}
              isRedirect={false}
            />
          </div >
        ))
      }
    </div >
  );
}
