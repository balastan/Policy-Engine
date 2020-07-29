package httpapi.authz


# By default, deny requests.
default allow = false

# Allow admins to do anything.
allow {
  user_is_chimpadmin
}

# allow {
#   group[objects] { objects := data.group_permissions[_]}
    
# }

# Allow the action if the user is granted permission to perform the action.
allow {
  group_private := data.group_permissions[input.object]["is_private"]
  group_private == "false"
}

allow {
  user_group_memberships = data.user_permissions[user_id]["group"]["member"]
  # lower(input.ability) != "manage"
  user_group_memberships[_] == input.object
}

allow {
  token.payload["https://myroles.com/roles"][_] == "GroupAdmin"
  user_group_admin = data.user_permissions[user_id]["group"]["admin"]
  user_group_admin[_] == input.object
}

# user_is_admin is true if...
user_is_chimpadmin {
  token.payload["https://myroles.com/roles"][_] == "ChimpAdmin"
}


token = {"payload": payload} {
  [header, payload, signature] := io.jwt.decode(input.token)
}

user_id = token.payload.sub