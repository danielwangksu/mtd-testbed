
template = %{
auto lo
iface lo inet loopback

<% for iface in interfaces %>
auto <%= iface.name %>
iface <%= iface.name %> inet static
	address <%= iface.address %>
	network <%= iface.network %>
	<% if iface.gateway %>
	gateway <%= iface.gateway %>
	<% end %>

<% end %>
}
