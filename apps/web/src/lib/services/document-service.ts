import { supabaseAdmin } from "../supabase/supabase-admin";

export async function buildGetAppByAppIdQuery(appId: string) {
  return supabaseAdmin
    .from("latest_app_view")
    .select("*")
    .eq("app_id", appId)
    .order("created_at", { ascending: false })
    .limit(1)
    .single();
}
