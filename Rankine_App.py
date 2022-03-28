import sys
from PyQt5 import QtWidgets as qtw
from Rankine_GUI import Ui_Form
from Rankine import rankine
from Steam import steam


class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        MainWindow constructor
        """
        super().__init__()
        self.setupUi(self)
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.show()

    def Calculate(self):
        p_highh = int(self.le_PHigh.text())
        p_loww = float(self.le_PLow.text())
        T_eff = float(self.le_TurbineEff.text())
        steam1 = steam(p_highh*100)
        steam2 = steam(p_loww*100)
        rankine1 = 0
        if self.rdo_Quality.isChecked():
            rankine1 = rankine(p_loww * 100, p_high=p_highh * 100, t_high=None, eff_turbine=T_eff)
            self.lbl_SatPropHigh.setText("Saturated Properties")
            self.lbl_SatPropLow.setText("Saturated Properties")
        else:
            rankine1 = rankine(p_loww * 100, p_high=p_highh * 100, t_high=500, eff_turbine=T_eff)
            self.lbl_SatPropHigh.setText("Super Heated Properties")
            self.lbl_SatPropLow.setText("Super Heated Properties")
        values1 = rankine1.calc_efficiency()
        p_high_values = steam1.calc()
        p_low_values = steam2.calc()
        h1, h2, h3, h4, T_work, P_work, H_added, Therm_eff = values1
        h_hf, h_hg, h_sf, h_sg, h_vf, h_vg = p_high_values
        l_hf, l_hg, l_sf, l_sg, l_vf, l_vg = p_low_values
        self.lbl_SatPropHigh.setText(f"PSat = {p_highh:.2f} bar, TSat = \u00B0 C\n"
                                     f"hf = {h_hf:.2f} kJ/kg, hg = {h_hg:.2f} kJ/kg\n"
                                     f"sf = {h_sf:.2f} kJ/kg*K, sg = {h_sg:.2f} kJ/kg*K\n"
                                     f"vf = {h_vf:.2f} m^3/kg, vg = {h_vg:.2f} m^3/kg")
        self.lbl_SatPropLow.setText(f"PSat = {p_loww:.2f} bar, TSat = \u00B0 C\n" 
                                    f"hf = {l_hf:.2f} kJ/kg, hg = {l_hg:.2f} kJ/kg\n"
                                    f"sf = {l_sf:.2f} kJ/kg*K, sg = {l_sg:.2f} kJ/kg*K\n"
                                    f"vf = {l_vf:.2f} m^3/kg, vg = {l_vg:.2f} m^3/kg")
        self.le_H1.setText(f"{h1:.2f}")
        self.le_H2.setText(f"{h2:.2f}")
        self.le_H3.setText(f"{h3:.2f}")
        self.le_H4.setText(f"{h4:.2f}")
        self.le_TurbineEff.setText(f"{T_work:.2f}")
        self.le_PumpWork.setText(f"{P_work:.2f}")
        self.le_HeatAdded.setText(f"{H_added:.2f}")
        self.le_Efficiency.setText(f"{Therm_eff:.2f}")


if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine Cycle Calculator')
    sys.exit(app.exec())