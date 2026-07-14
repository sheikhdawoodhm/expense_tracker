import { Component, signal, computed, inject } from '@angular/core'; 
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LedgerService, TrackerItem, TrackerType } from '../../services/ledger.service'; 

@Component({
  selector: 'app-expense-tracker',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './expense-tracker.component.html',
})
export class ExpenseTrackerComponent {
  private ledgerService = inject(LedgerService); 

  activeType = signal<TrackerType>('expense');
  isEditing = signal<boolean>(false);
  editingId = signal<string | null>(null);

  categoriesMap = signal<{ [key in TrackerType]: string[] }>({
    expense: ['Food', 'Rent', 'Utilities', 'Entertainment'],
    asset: ['Stocks', 'Savings Account', 'Real Estate', 'Crypto'],
    liability: ['Credit Card', 'Mortgage', 'Student Loan', 'Car Loan']
  });

  newCategoryName = '';
  showCustomInput = false;

  currentCategories = computed(() => this.categoriesMap()[this.activeType()]);
  
  
  items = this.ledgerService.items; 

  netBalance = computed(() => {
    return this.items().reduce((total, item) => {
      return item.type === 'asset' ? total + item.amount : total - item.amount;
    }, 0);
  });

  formData = {
    title: '',
    amount: 0,
    category: 'Food'
  };

  changeType(type: TrackerType) {
    this.activeType.set(type);
    this.formData.category = this.categoriesMap()[type][0];
    this.showCustomInput = false; 
  }

  addCustomCategory() {
    const trimmed = this.newCategoryName.trim();
    if (!trimmed) return;

    const formattedCategory = trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
    const currentMap = this.categoriesMap();
    const currentType = this.activeType();

    if (!currentMap[currentType].includes(formattedCategory)) {
      this.categoriesMap.update(prev => ({
        ...prev,
        [currentType]: [...prev[currentType], formattedCategory]
      }));
    }

    this.formData.category = formattedCategory;
    this.newCategoryName = '';
    this.showCustomInput = false;
  }

  saveItem() {
    if (this.isEditing()) {
      this.items.update(prev => prev.map(item => 
        item.id === this.editingId() 
          ? { ...item, ...this.formData, type: this.activeType() } 
          : item
      ));
      this.resetForm();
    } else {
      const newItem: TrackerItem = {
        id: crypto.randomUUID(),
        type: this.activeType(),
        title: this.formData.title,
        amount: this.formData.amount,
        category: this.formData.category,
        date: new Date()
      };
      this.items.update(prev => [...prev, newItem]); 
      this.resetForm();
    }
  }

  editItem(item: TrackerItem) {
    this.isEditing.set(true);
    this.editingId.set(item.id);
    this.activeType.set(item.type);
    this.formData = {
      title: item.title,
      amount: item.amount,
      category: item.category
    };
  }

  deleteItem(id: string) {
    this.items.update(prev => prev.filter(item => item.id !== id));
    if (this.editingId() === id) this.resetForm();
  }

  resetForm() {
    this.isEditing.set(false);
    this.editingId.set(null);
    this.formData = { 
      title: '', 
      amount: 0, 
      category: this.categoriesMap()[this.activeType()][0]
    };
  }
}