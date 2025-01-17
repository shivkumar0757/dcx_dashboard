from rest_framework import serializers

class PositionSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    pair = serializers.CharField(max_length=50)
    active_pos = serializers.FloatField()
    inactive_pos_buy = serializers.FloatField()
    inactive_pos_sell = serializers.FloatField()
    avg_price = serializers.FloatField()
    liquidation_price = serializers.FloatField()
    locked_margin = serializers.FloatField()
    locked_user_margin = serializers.FloatField()
    locked_order_margin = serializers.FloatField()
    take_profit_trigger = serializers.FloatField(allow_null=True)
    stop_loss_trigger = serializers.FloatField(allow_null=True)
    leverage = serializers.FloatField()
    maintenance_margin = serializers.FloatField()
    mark_price = serializers.FloatField()
    margin_type = serializers.CharField(max_length=50, allow_null=True)
    updated_at = serializers.IntegerField()
    pnl = serializers.FloatField()
    roe = serializers.FloatField()
    margin_currency = serializers.CharField(max_length=10)
