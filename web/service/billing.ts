import type { CurrentPlanInfoBackend, SubscriptionUrlsBackend } from '@/app/components/billing/type'
import { get } from './base'

type CurrentPlanInfoResponse = Omit<CurrentPlanInfoBackend, 'workspace_members'> & {
  workspace_members: Omit<CurrentPlanInfoBackend['workspace_members'], 'size'> & {
    size: number | null
  }
}

export const fetchCurrentPlanInfo = async (): Promise<CurrentPlanInfoBackend> => {
  const data = await get<CurrentPlanInfoResponse>('/features')

  return {
    ...data,
    workspace_members: {
      ...data.workspace_members,
      size: data.workspace_members.size ?? 0,
    },
  }
}

export const fetchSubscriptionUrls = (plan: string, interval: string) => {
  return get<SubscriptionUrlsBackend>(`/billing/subscription?plan=${plan}&interval=${interval}`)
}
