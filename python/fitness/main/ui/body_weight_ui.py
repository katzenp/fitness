"""
body_weight_ui.py

Description:
    User interface for registering/tracking an individual's body metrics
        - body_fat
        - muscle size

    SIZE_DATA = {
        'date': {
            'l_wrist': 0.00,
            'r_wrist': 0.00,
            'l_forearm': 0.00,
            'r_forearm': 0.00,
            'l_bicep': 0.00,
            'r_bicep': 0.00,
            'l_ankle': 0.00,
            'r_ankle': 0.00,
            'l_calf': 0.00,
            'r_calf': 0.00,
            'l_thigh': 0.00,
            'r_thigh': 0.00,
            'waist': 0.00,
            'chest': 0.00,
            'neck': 0.00}}
"""
# Python standard libraries
import os
import re
import sys

# Qt libraries
from PySide import QtGui, QtCore

# local libraries
import python.main.body_weight as body_weight


# ==============================================================================
# constants / globals
# ==============================================================================
MODE_UNITS = {'imperial': {'height': 'in.',
                           'weight': 'lbs.'},
              'metric': {'height': 'cm.',
                         'weight': 'kg.'}}
GENDERS = ('male', 'female')

TEMPLATE_ROOT = os.path.realpath(__file__)
TEMPLATE_ROOT = os.path.dirname(TEMPLATE_ROOT)
WEIGHT_LOG_TEMPLATE = os.path.join(TEMPLATE_ROOT, 'resources', 'weight_log_template.html')


# ==============================================================================
# Body Weight
# ==============================================================================
def getWeightLogDocument(height_cm, weight_kg, age, body_fat, male, equation, modifier):
    """
    Generates an HTML document representing a person's weight log based on the
    given body metrics

    :param height_cm: your height in centimeters
    :type height_cm: float
    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param age: your age in years
    :type age: int
    :param body_fat: your body fat percentage expressed as an integer
    :type body_fat: int
    :param male: is the calculation being performed for a male?
    :type male: bool
    :param equation: name of  basal metabolic rate equation to use.
                     Must be one of the following:
                        'harrisBenedict', 'mifflinStJeor', 'katchMcArdle', or None
                     if None, an average value will be used
    :type equation: string, None
    :param modifier: number representing how physically active you are
                     Adjusts your basal metabolic rate to reflect the number of
                     calories burned through exercise (total daily energy expenditure)
    :type modifier: float in range 1.0 - 1.50
    :return: html document
    :rtype: string
    """
    # compute data
    weight_data = body_weight.getWeightData(height_cm, weight_kg, age, body_fat, male, equation, modifier, precision=2)
    weight_kg = weight_data.get('weight', 'undefined')
    weight_units = 'kg'
    body_fat = weight_data.get('bf', 'undefined')
    lbm = weight_data.get('lbm', 'undefined')
    bmr = weight_data.get('bmr', 'undefined')
    bmr_multiplier = modifier
    tdee = weight_data.get('tdee', 'undefined')

    # compute macros data
    macros_data = body_weight.getMacrosData(weight_kg)
    cut = macros_data.get("cut", {}).get("total", 0.0)
    maintain = macros_data.get("maintain", {}).get("total", 0.0)
    gain = macros_data.get("bulk", {}).get("total", 0.0)

    # generate document
    document = ''
    with open(WEIGHT_LOG_TEMPLATE, 'r') as infile:
        document = infile.read()

    old = re.findall("<style.*style>", document, re.DOTALL)
    if old:
        new = old[0].replace('{', '{{')
        new = new.replace('}', '}}')
        document = document.replace(old[0], new)

    document = document.format(weight=weight_kg,
                               weight_units=weight_units,
                               body_fat=body_fat,
                               lbm=lbm,
                               bmr=bmr,
                               bmr_multiplier=bmr_multiplier,
                               tdee=tdee,
                               cut=cut,
                               maintain=maintain,
                               bulk=gain)
    return document


class Body_Weight_Table(QtGui.QTableWidget):
    """
    QTableWidget for displaying body weight information

    Public Attributes:
        None
    """
    def __init__(self, data=(), parent=None):
        """
        Constructor method

        :param data: list of tuples representing the rows of data to display
        :type data: list of tuples
        :param parent: this widgets parent object
        :type parent: instance of <class 'QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(Body_Weight_Table, self).__init__(parent=parent)
        self.setAlternatingRowColors(True)
        self._data = data

        self._buildUi()

    def _buildUi(self):
        """
        Defines and organized all of this ui's elements

        :return: n/a
        :rtype: n/a
        """
        for r, row_data in enumerate(self._data):
            self.insertRow(r)
            for c, column_data in enumerate(row_data):
                if r == 0:
                    self.insertColumn(c)
                item = QtGui.QTableWidgetItem(column_data)
                self.setItem(r, c, item)


class Body_Weight_Widget(QtGui.QWidget):
    """
    User interface for entering in and recording personal body weight metrics

    Public Attributes:
        :attr age: age data associated with this widget
        :type age: int
        :attr height: height data associated with this widget
        :type height: float
        :attr weight: body weight data associated with this widget
        :type weight: float
        :attr body_fat: body_fat data associated with this widget
        :type body_fat: float
        :attr gender: gender data associated with this widget
        :type gender: string
        :attr mode: measurement system data associated with this widget
        :type mode: string
    """
    def __init__(self, mode='imperial', parent=None):
        """
        Constructor method

        :param mode: unit of measurement mode (metric/imperial)
        :type mode: string
        :param parent: this widgets parent object
        :type parent: instance of <class 'QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(Body_Weight_Widget, self).__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # body metrics
        self._age = 1
        self._height = 0.0
        self._weight = 0.0
        self._body_fat = 0.0
        self._gender = 'male'
        self._mode = mode

        # ui setup
        self._buildUi()
        self._connectSignals()
        self._initializeUi()

    # --------------------------------------------------------------------------
    # managed attributes
    # --------------------------------------------------------------------------
    @property
    def age(self):
        """
        Returns the age data associated with this widget

        :return: age data associated with this widget
        :rtype: int
        """
        return self._age

    @property
    def height(self):
        """
        Returns the height data associated with this widget

        :return: height data associated with this widget
        :rtype: float
        """
        return self._height

    @property
    def weight(self):
        """
        Returns the body weight data associated with this widget

        :return: body weight data associated with this widget
        :rtype: float
        """
        return self._weight

    @property
    def body_fat(self):
        """
        Returns the body_fat data associated with this widget

        :return: body_fat data associated with this widget
        :rtype: float
        """
        return self._body_fat

    @property
    def gender(self):
        """
        Returns the gender data associated with this widget

        :return: gender data associated with this widget
        :rtype: string 
        """
        return self._gender

    @property
    def mode(self):
        """
        Returns the measurement system data associated with this widget

        :return: measurement system data associated with this widget
        :rtype: string
        """
        return self._mode

    # --------------------------------------------------------------------------
    # slots
    # --------------------------------------------------------------------------
    def _units_chosen(self):
        """
        aaction taken whenever the user selects a new uint of measurement

        :return: n/a
        :rtype: n/a
        """
        sender = self.sender()

        # get current state/values
        mode = self._mode
        height = self.height_field.value()
        weight = self.weight_field.value()

        # update widgets
        if sender == self.imperial_button:
            self.height_units_label.setText('in')
            self.weight_units_label.setText('lb')
            self._mode = 'imperial'
        else:
            self.height_units_label.setText('cm')
            self.weight_units_label.setText('kg')
            self._mode = 'metric'

        # convert values
        if mode == 'metric' and self._mode == 'imperial':
            self._height = height / 2.54
            self._weight = weight / 0.454
        elif mode == 'imperial' and self._mode == 'metric':
            self._height = height * 2.54
            self._weight = weight * 0.454

        # update data widgets
        self.height_field.setValue(self._height)
        self.weight_field.setValue(self._weight)

    def _age_changed(self, value):
        """
        Actions taken whenever the user changes the age field

        :param value: value entered by the user
        :type value: float
        :return: n/a
        :rtype: n/a
        """
        # update internal data
        self._age = value

    def _height_changed(self, value):
        """
        Actions taken whenever the user changes the height field

        :param value: value entered by the user
        :type value: float
        :return: n/a
        :rtype: n/a
        """
        # update internal data
        self._height = value

    def _weight_changed(self, value):
        """
        Actions taken whenever the user changes the weight field

        :param value: value entered by the user
        :type value: float
        :return: n/a
        :rtype: n/a
        """
        # update internal data
        self._weight = value

    def _bodyFat_changed(self, value):
        """
        Actions taken whenever the user changes the bodyFat field

        :param value: value entered by the user
        :type value: float
        :return: n/a
        :rtype: n/a
        """
        # update internal data
        self._body_fat = value

    def _gender_changed(self, index):
        """
        Actiosn taken whenever the user selects a new gender

        :param index: list index of the currently selected gender
        :type index:
        :return: n/a
        :rtype: n/a
        """
        # update internal data
        self._gender = GENDERS[index]

    def _calculate_feedback(self):
        """
        Calculates relevant body metrics based on the data supplied by the user
        and displays it in the feedback field

        :return: n/a
        :rtype: n/a
        """
        age = self.age_field.value()
        height_cm = self.height_field.value()
        weight_kg = self.weight_field.value()
        body_fat = self.bodyFat_field.value()
        male = bool(self.gender_combobox.currentIndex())

        if self._mode != 'metric':
            height_cm *= 2.54
            weight_kg *= 0.454

        document = getWeightLogDocument(height_cm, weight_kg, age, body_fat, male, None, 1.2)
        self.feedback_field.setHtml(document)

    # --------------------------------------------------------------------------
    # ui set up
    # --------------------------------------------------------------------------
    def _buildUi(self):
        """
        Defines and organized all of this ui's elements

        :return: n/a
        :rtype: n/a
        """
        # units
        self.units_label = QtGui.QLabel('Units: ')
        self.units_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.imperial_button = QtGui.QRadioButton('imperial')
        self.metric_button = QtGui.QRadioButton('metric')

        self.unit_buttons_group = QtGui.QButtonGroup()
        self.unit_buttons_group.addButton(self.imperial_button)
        self.unit_buttons_group.addButton(self.metric_button)
        self.unit_buttons_group.setExclusive(True)

        # age
        self.age_label = QtGui.QLabel('Age: ')
        self.age_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.age_field = QtGui.QDoubleSpinBox()
        self.age_field.setFixedWidth(70)
        self.age_field.setRange(1, 200)
        self.age_field.setSingleStep(1)
        self.age_field.setValue(self._age)

        # height
        self.height_label = QtGui.QLabel('Height: ')
        self.height_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.height_field = QtGui.QDoubleSpinBox()
        self.height_field.setFixedWidth(70)
        self.height_field.setRange(1, 1000)
        self.height_field.setSingleStep(0.1)
        self.height_field.setValue(self._height)
        self.height_units_label = QtGui.QLabel()

        # weight
        self.weight_label = QtGui.QLabel('Weight: ')
        self.weight_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.weight_field = QtGui.QDoubleSpinBox()
        self.weight_field.setFixedWidth(70)
        self.weight_field.setRange(1, 2000)
        self.weight_field.setSingleStep(0.1)
        self.weight_field.setValue(self._weight)
        self.weight_units_label = QtGui.QLabel()

        # body fat
        self.bodyFat_label = QtGui.QLabel('Body Fat %: ')
        self.bodyFat_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.bodyFat_field = QtGui.QDoubleSpinBox()
        self.bodyFat_field.setFixedWidth(70)
        self.bodyFat_field.setRange(1, 100)
        self.bodyFat_field.setSingleStep(0.1)
        self.bodyFat_field.setValue(self._body_fat)

        # gender
        self.gender_label = QtGui.QLabel('Gender: ')
        self.gender_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.gender_combobox = QtGui.QComboBox()
        self.gender_combobox.addItems(GENDERS)

        # data display
        self.calculate_button = QtGui.QPushButton('Calculate ...')
        self.calculate_button.setFixedHeight(35)
        self.feedback_field = QtGui.QTextEdit()

        # data entry lyout
        self.data_entry_grid = QtGui.QGridLayout()
        self.data_entry_grid.setSpacing(4)
        self.data_entry_grid.setContentsMargins(6, 6, 6, 6)
        self.data_entry_grid.addWidget(self.age_label, 0, 0, 1, 1)
        self.data_entry_grid.addWidget(self.age_field, 0, 1, 1, 1)
        self.data_entry_grid.addWidget(self.height_label, 1, 0, 1, 1)
        self.data_entry_grid.addWidget(self.height_field, 1, 1, 1, 1)
        self.data_entry_grid.addWidget(self.height_units_label, 1, 2, 1, 1)
        self.data_entry_grid.addWidget(self.weight_label, 2, 0, 1, 1)
        self.data_entry_grid.addWidget(self.weight_field, 2, 1, 1, 1)
        self.data_entry_grid.addWidget(self.weight_units_label, 2, 2, 1, 1)
        self.data_entry_grid.addWidget(self.bodyFat_label, 3, 0, 1, 1)
        self.data_entry_grid.addWidget(self.bodyFat_field, 3, 1, 1, 1)
        self.data_entry_grid.addWidget(self.gender_label, 4, 0, 1, 1)
        self.data_entry_grid.addWidget(self.gender_combobox, 4, 1, 1, 1)
        self.data_entry_grid.addWidget(self.units_label, 5, 0, 1, 1)
        self.data_entry_grid.addWidget(self.imperial_button, 5, 1, 1, 1)
        self.data_entry_grid.addWidget(self.metric_button, 5, 2, 1, 1)

        self.data_entry_grid.setColumnStretch(0, 0)
        self.data_entry_grid.setColumnStretch(1, 0)
        self.data_entry_grid.setColumnStretch(2, 0)
        self.data_entry_grid.setColumnStretch(3, 1)

        # main layout
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addLayout(self.data_entry_grid)
        self.main_layout.addWidget(self.calculate_button)
        self.main_layout.addWidget(self.feedback_field)
        self.setLayout(self.main_layout)

    def _initializeUi(self):
        """
        Initializes all relevant widget values and settings

        :return: n/a
        :rtype: n/a
        """
        if self._mode == 'imperial':
            self.imperial_button.setChecked(True)
            self.imperial_button.clicked.emit()
        else:
            self.metric_button.setChecked(True)
            self.metric_button.clicked.emit()

    def _connectSignals(self):
        """
        Defines all SIGNAL/SLOT connections

        :return: n/a
        :rtype: n/a
        """
        self.imperial_button.clicked.connect(self._units_chosen)
        self.metric_button.clicked.connect(self._units_chosen)
        self.age_field.valueChanged.connect(self._age_changed)
        self.height_field.valueChanged.connect(self._height_changed)
        self.weight_field.valueChanged.connect(self._weight_changed)
        self.bodyFat_field.valueChanged.connect(self._bodyFat_changed)
        self.gender_combobox.currentIndexChanged.connect(self._gender_changed)
        self.calculate_button.clicked.connect(self._calculate_feedback)


if __name__ == '__main__':
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(sys.argv)

    bww = Body_Weight_Widget()
    bww.show()

    app.exec_()
