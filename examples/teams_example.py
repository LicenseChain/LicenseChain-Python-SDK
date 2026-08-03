#!/usr/bin/env python3
"""
LicenseChain Python SDK - Teams Example

This example demonstrates how to use team collaboration features
available to Pro, Business, and Enterprise tier users.
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from licensechain.client import LicenseChainClient


async def main():
    """Main example function."""
    print("👥 LicenseChain Python SDK - Teams Example\n")
    
    # Initialize the client
    api_key = os.getenv('LICENSECHAIN_API_KEY', 'your-api-key-here')
    client = LicenseChainClient(
        api_key=api_key,
        base_url='https://api.licensechain.app/v1',
        timeout=30,
        retry_attempts=3,
    )
    
    try:
        # 1. List Teams
        print("📋 Listing Teams...")
        teams_response = await client.list_teams()
        
        if teams_response.get('success'):
            teams = teams_response.get('teams', [])
            print(f"\n✅ Found {len(teams)} teams")
            
            for team in teams:
                print(f"\n   Team: {team.get('name', 'N/A')}")
                print(f"   ID: {team.get('id', 'N/A')}")
                print(f"   Your Role: {team.get('userRole', 'N/A')}")
                if team.get('description'):
                    print(f"   Description: {team.get('description', '')[:50]}...")
                
                # Team Statistics
                counts = team.get('_count', {})
                print(f"   Members: {counts.get('members', 0)}")
                print(f"   Apps: {counts.get('appAccess', 0)}")
                print(f"   Licenses: {counts.get('licenseAccess', 0)}")
        else:
            print(f"❌ Failed to list teams: {teams_response.get('error', 'Unknown error')}")
            print("⚠️  Team collaboration requires Pro, Business, or Enterprise tier")
            return
        
        # 2. Create a Team
        print("\n➕ Creating a New Team...")
        try:
            new_team = await client.create_team(
                name="Development Team",
                description="Team for development and testing",
            )
            
            if new_team.get('success'):
                team = new_team.get('team', {})
                print(f"✅ Team Created:")
                print(f"   ID: {team.get('id', 'N/A')}")
                print(f"   Name: {team.get('name', 'N/A')}")
                print(f"   Your Role: {team.get('userRole', 'N/A')}")
                
                team_id = team.get('id')
                
                # 3. Get Team Details
                if team_id:
                    print(f"\n📋 Getting Team Details...")
                    team_details = await client.get_team(team_id)
                    
                    if team_details.get('success'):
                        team = team_details.get('team', {})
                        print(f"✅ Team Details:")
                        print(f"   Name: {team.get('name', 'N/A')}")
                        print(f"   Description: {team.get('description', 'N/A')}")
                        
                        # List Members
                        members = team.get('members', [])
                        if members:
                            print(f"\n   Members ({len(members)}):")
                            for member in members:
                                user = member.get('user', {})
                                print(f"      - {user.get('name', 'N/A')} ({user.get('email', 'N/A')})")
                                print(f"        Role: {member.get('role', 'N/A')}")
                                print(f"        Status: {member.get('status', 'N/A')}")
                
                # 4. Invite Team Member
                if team_id:
                    print(f"\n📧 Inviting Team Member...")
                    # Note: Replace with actual email address
                    invite_email = "member@example.com"
                    try:
                        invite_response = await client.invite_team_member(
                            team_id=team_id,
                            email=invite_email,
                            role="member",
                        )
                        
                        if invite_response.get('success'):
                            print(f"✅ Invitation sent to {invite_email}")
                        else:
                            print(f"⚠️  Failed to send invitation: {invite_response.get('error', 'Unknown error')}")
                    except Exception as e:
                        print(f"⚠️  Invitation error (may need valid email): {type(e).__name__}")
                
                # 5. List Team Members
                if team_id:
                    print(f"\n👥 Listing Team Members...")
                    members_response = await client.list_team_members(team_id)
                    
                    if members_response.get('success'):
                        members = members_response.get('members', [])
                        print(f"✅ Team has {len(members)} members")
                        for member in members:
                            user = member.get('user', {})
                            print(f"   - {user.get('name', 'N/A')} ({user.get('email', 'N/A')}) - {member.get('role', 'N/A')}")
                
                # 6. Share App with Team
                if team_id:
                    print(f"\n📱 Sharing App with Team...")
                    # First, get a list of apps
                    apps_response = await client.list_applications(limit=1)
                    if apps_response.get('apps') and len(apps_response['apps']) > 0:
                        app_id = apps_response['apps'][0].get('id')
                        if app_id:
                            try:
                                share_response = await client.share_app_with_team(
                                    team_id=team_id,
                                    app_id=app_id,
                                )
                                
                                if share_response.get('success'):
                                    print(f"✅ App {app_id} shared with team")
                                else:
                                    print(f"⚠️  Failed to share app: {share_response.get('error', 'Unknown error')}")
                            except Exception as e:
                                print(f"⚠️  Share app error: {type(e).__name__} - {e}")
                
                # 7. List Team Apps
                if team_id:
                    print(f"\n📱 Listing Team Apps...")
                    team_apps_response = await client.list_team_apps(team_id)
                    
                    if team_apps_response.get('success'):
                        apps = team_apps_response.get('apps', [])
                        print(f"✅ Team has access to {len(apps)} apps")
                        for app in apps:
                            print(f"   - {app.get('name', 'N/A')} (ID: {app.get('id', 'N/A')})")
                
                # 8. Update Team
                if team_id:
                    print(f"\n✏️  Updating Team...")
                    updated_team = await client.update_team(
                        team_id=team_id,
                        description="Updated: Development team for all projects",
                    )
                    
                    if updated_team.get('success'):
                        team = updated_team.get('team', {})
                        print(f"✅ Team Updated:")
                        print(f"   Description: {team.get('description', 'N/A')}")
                
                # 9. Cleanup - Delete Team (if you're the owner)
                # Uncomment to delete the team
                # if team_id:
                #     print(f"\n🗑️  Deleting Team...")
                #     delete_response = await client.delete_team(team_id)
                #     if delete_response.get('success'):
                #         print(f"✅ Team Deleted")
            else:
                print(f"❌ Failed to create team: {new_team.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"⚠️  Team operations require Pro+ tier: {type(e).__name__} - {e}")
        
        print("\n✅ Teams example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__} - {e}")
        if os.getenv('DEBUG'):
            import traceback
            traceback.print_exc()
    
    finally:
        # Cleanup
        await client.close()
        print("\n🔌 Client closed")


if __name__ == '__main__':
    asyncio.run(main())
