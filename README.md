# Wiegand's Tree Sales Assistant — POC v14

## Fixes the broad-choice layer

v13 had an initialization bug: the app tried to assign `sales_group` before the grouping function was defined.

v14 fixes that and also persists the Find Trees state across Streamlit reruns.

Expected flow:
1. Enter criteria and tap **Find Trees**.
2. See **Broad Choices That Fit the Customer** such as Serviceberry, Hydrangea Tree on Standard, Japanese Maple, Japanese Tree Lilac, Redbud, etc.
3. Select one or more broad choices.
4. Review the matching cultivars in those groups.

The Full Match / Partial Match / May Fit logic is unchanged.
