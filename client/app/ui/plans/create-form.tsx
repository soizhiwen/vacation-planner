'use client';

import Form from 'next/form'
import { useActionState } from 'react';
import { createPlan, State } from '@/app/lib/actions';

export default function CreateForm() {
  const initialState: State = { errors: {}, message: null };
  const [state, formAction] = useActionState(createPlan, initialState);

  return (
    <Form action={formAction}>
      <div>
        <label htmlFor="budget">
          Budget
        </label>
        <input
          id="budget"
          name="budget"
          placeholder="Enter USD budget"
          aria-describedby="budget-error"
          required
        />
        <div id="budget-error" aria-live="polite" aria-atomic="true">
          {state.errors?.budget &&
            state.errors.budget.map((error: string) => (
              <p key={error}>
                {error}
              </p>
            ))}
        </div>
      </div>
      <div>
        <label htmlFor="total-days">
          Total Days
        </label>
        <input
          id="total-days"
          name="totalDays"
          placeholder="Enter total days"
          aria-describedby="total-days-error"
          required
        />
        <div id="total-days-error" aria-live="polite" aria-atomic="true">
          {state.errors?.totalDays &&
            state.errors.totalDays.map((error: string) => (
              <p key={error}>
                {error}
              </p>
            ))}
        </div>
      </div>
      <div id="message-error" aria-live="polite" aria-atomic="true">
        {state.message &&
          <p key={state.message}>
            {state.message}
          </p>
        }
      </div>
      <button type="submit">
        Generate
      </button>
    </Form>
  );
}
