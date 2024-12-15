import { z } from 'zod';


export const CreatePlanFormSchema = z.object({
    budget: z.coerce
        .number({ message: 'Invalid Budget.' })
        .int({ message: 'Budget must be a number.' })
        .nonnegative({ message: 'Please enter an amount greater than $0.' }),
    totalDays: z.coerce
        .number({ message: 'Invalid Total Days.' })
        .int({ message: 'Total Days must be a number.' })
        .nonnegative({ message: 'Please enter a number greater than 0.' }),
});