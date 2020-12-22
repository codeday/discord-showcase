from discord.ext.commands import Context, check, MissingAnyRole
import json
import os


def requires_staff_role():
    """A check that scans for a staff role. Staff roles must be updated here, which isn't that obvious,
    but it will try to pull from env vars, then fall back to the staff role listed.
    """
    async def predicate(ctx: Context):
        # Current "Staff", "Employee", and Test Server Admin roles ID as of 12/22/20
        staff_id = json.loads(os.getenv("ROLES_STAFF", '["689215241996730417", "712062910897061979", '
                                                       '"704392406434447360"]'))
        if [i for i in [str(role.id) for role in ctx.author.roles] if i in staff_id]:
            return True
        raise MissingAnyRole(staff_id)
    return check(predicate)
