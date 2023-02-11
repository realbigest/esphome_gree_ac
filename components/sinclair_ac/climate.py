#based on: https://github.com/DomiStyle/esphome-panasonic-ac

from esphome.const import (
    CONF_ID,
)
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, climate, sensor, select, switch

AUTO_LOAD = ["switch", "sensor", "select"]
DEPENDENCIES = ["uart"]

sinclair_ac_ns = cg.esphome_ns.namespace("sinclair_ac")
SinclairAC = sinclair_ac_ns.class_(
    "SinclairAC", cg.Component, uart.UARTDevice, climate.Climate
)
sinclair_ac_cnt_ns = sinclair_ac_ns.namespace("CNT")
SinclairACCNT = sinclair_ac_cnt_ns.class_("SinclairACCNT", SinclairAC)

SinclairACSwitch = sinclair_ac_ns.class_(
    "SinclairACSwitch", switch.Switch, cg.Component
)
SinclairACSelect = sinclair_ac_ns.class_(
    "SinclairACSelect", select.Select, cg.Component
)


CONF_HORIZONTAL_SWING_SELECT = "horizontal_swing_select"
CONF_VERTICAL_SWING_SELECT = "vertical_swing_select"

CONF_CURRENT_TEMPERATURE_SENSOR = "current_temperature_sensor"

HORIZONTAL_SWING_OPTIONS = [
    "0 - OFF",
    "1 - Swing - Full",
    "2 - Constant - Left",
    "3 - Constant - Mid-Left",
    "4 - Constant - Middle",
    "5 - Constant - Mid-Right",
    "6 - Constant - Right",
]


VERTICAL_SWING_OPTIONS = [
    "00 - OFF",
    "01 - Swing - Full",
    "02 - Swing - Down",
    "03 - Swing - Mid-Down",
    "04 - Swing - Middle",
    "05 - Swing - Mid-Up",
    "06 - Swing - Up",
    "07 - Constant - Down",
    "08 - Constant - Mid-Down",
    "09 - Constant - Middle",
    "10 - Constant - Mid-Up",
    "11 - Constant - Up",
]

SWITCH_SCHEMA = switch.SWITCH_SCHEMA.extend(cv.COMPONENT_SCHEMA).extend(
    {cv.GenerateID(): cv.declare_id(SinclairACSwitch)}
)
SELECT_SCHEMA = select.SELECT_SCHEMA.extend(
    {cv.GenerateID(CONF_ID): cv.declare_id(SinclairACSelect)}
)

SCHEMA = climate.CLIMATE_SCHEMA.extend(
    {
        cv.Optional(CONF_HORIZONTAL_SWING_SELECT): SELECT_SCHEMA,
        cv.Optional(CONF_VERTICAL_SWING_SELECT): SELECT_SCHEMA,
    }
).extend(uart.UART_DEVICE_SCHEMA)

CONFIG_SCHEMA = cv.All(
    SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(SinclairACCNT),
            cv.Optional(CONF_CURRENT_TEMPERATURE_SENSOR): cv.use_id(sensor.Sensor),
        }
    ),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await climate.register_climate(var, config)
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_HORIZONTAL_SWING_SELECT in config:
        conf = config[CONF_HORIZONTAL_SWING_SELECT]
        swing_select = await select.new_select(conf, options=HORIZONTAL_SWING_OPTIONS)
        await cg.register_component(swing_select, conf)
        cg.add(var.set_horizontal_swing_select(swing_select))

    if CONF_VERTICAL_SWING_SELECT in config:
        conf = config[CONF_VERTICAL_SWING_SELECT]
        swing_select = await select.new_select(conf, options=VERTICAL_SWING_OPTIONS)
        await cg.register_component(swing_select, conf)
        cg.add(var.set_vertical_swing_select(swing_select))

    if CONF_CURRENT_TEMPERATURE_SENSOR in config:
        sens = await cg.get_variable(config[CONF_CURRENT_TEMPERATURE_SENSOR])
        cg.add(var.set_current_temperature_sensor(sens))
